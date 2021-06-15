#coding: utf-8
import time
import copy

from typing import Dict,Any

from .utils import (load_data, get_chrome_driver, 
                    try_find_element_click, try_find_element_send_keys)

class UtokyoHealthManagementReportForm():
    """If you want to create your own gateway class, please inherit this class.

    Args:
        path (str)     : Path to json data that describes the procedure of form.
        verbose (bool) : Whether to print message or not. (default= ``True`` )

    Attributes:
        print (function) : Print function according to ``verbose``
        data (dict)      : Data that describes the procedure of form.
        path (str)       : Path to json data that describes the procedure of form.
    """
    def __init__(self, path:str, verbose:bool=True, **kwargs):
        self.verbose:bool       = verbose
        self.print:callable     = print if verbose else lambda *args: None
        self.data:Dict[str,Any] = load_data(path)
        self.path:str           = path

    @staticmethod
    def answer_question(qno:str, ans_data={}, inputElements=[]):
        """Answer each question.

        Args:
            qno (str)            : Question number in the form.
            inputElements (list) : List of input elements in the form.
        """
        ans = ans_data.get(qno, {})
        no  = int(ans.get("no", 1))
        val = ans.get("val", "")

        target = inputElements[no-1]
        type = target.get_attribute("type")
        if type == "radio":
            target.click()
        elif type == "checkbox":
            for n in set(val + [no]):
                inputElements[int(n)-1].click()
        elif type == "text":
            if not isinstance(val, str):
                val = ",".join(val)
            target.send_keys(val)

    def login(self, driver, url, login_data={}):
        """Perform the login procedure required to answer the form.

        Args:
            driver (WebDriver) : Selenium WebDriver.
            url (str)          : URL of the form.
            login_data (dict)  : Data required for login.
        """
        self.print("[START LOGIN]")
        driver.get(url)
        login_data = copy.deepcopy(sorted(login_data.items(), key=lambda x:x[0]))
        for no,values in login_data:
            {
                "click" : try_find_element_click,
                "send_keys" : try_find_element_send_keys,
            }[values.pop("func")](driver=driver, verbose=self.verbose, **values)
        self.print("[END LOGIN]")

    def run(self, **kwargs):
        """
        Args:
            browser (bool) : Whether you want to run Chrome with GUI browser. (default= ``False`` )
        """
        with get_chrome_driver() as driver:
            self.login(driver=driver, url=self.data["URL"], login_data=self.data.get("login", {}))
            self.answer_form(driver=driver, **kwargs)

    def answer_form(self, driver, **kwargs):
        self.print("[START ANSWERING FORM]")
        ans_data = self.data.get("answer", {})
        answered_qnos = []
        not_found_count=0
        self.print("[START FORM]")
        while True:
            visible_questions = driver.find_elements_by_class_name(name="office-form-question")
            if len(answered_qnos) == 0:
                if not_found_count>5: break
                time.sleep(1)
                not_found_count += 1
            elif len(answered_qnos) == len(visible_questions): 
                break
            for question in visible_questions:
                # NOTE: question number depends on forms.
                qno = int(question.find_element_by_css_selector("span.ordinal-number").text.rstrip("."))
                if qno not in answered_qnos:
                    self.print(question.find_element_by_css_selector("div.question-title-box").text+"\n")
                    inputElements = question.find_elements_by_tag_name(name="input")
                    num_inputElements = len(inputElements)
                    for j,inputTag in enumerate(inputElements):
                        type_ = inputTag.get_attribute("type")
                        value = inputTag.get_attribute("value")
                        # NOTE: input no is 1-based index.
                        self.print(f"\t{j+1:>0{len(str(num_inputElements))}} [{type_}] {value}")
                    self.answer_question(qno=str(qno), ans_data=ans_data, inputElements=inputElements)
                    answered_qnos.append(qno)
                    self.print("-"*30)
        self.print("[END FORM]")
        try_find_element_click(driver=driver, by="css selector", identifier="button.__submit-button__", verbose=self.verbose)     
        self.print("[END ANSWERING FORM]")  
