# coding: utf-8
import copy
import time
from typing import Any, Dict, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .utils import (
    get_chrome_driver,
    load_data,
    try_find_element_click,
    try_find_element_send_keys,
)


class UtokyoHealthManagementReportForm:
    """If you want to create your own gateway class, please inherit this class.

    Args:
        path (str)     : Path to json data that describes the procedure of form.
        verbose (bool) : Whether to print message or not. Defaults to ``True``.

    Attributes:
        verbose (bool)   : Whether to print message or not. Defaults to ``True``.
        print (callable) : Print function according to ``verbose``
        data (dict)      : Data that describes the procedure of form.
        path (str)       : Path to json data that describes the procedure of form.
    """

    def __init__(self, path: str, verbose: bool = True, **kwargs):
        self.verbose: bool = verbose
        self.print: callable = print if verbose else lambda *args: None
        self.data: Dict[str, Any] = load_data(path)
        self.path: str = path

    @staticmethod
    def answer_question(
        question_number: str,
        answer_data: Dict[str, Dict[str, Any]] = {},
        inputElements: List[WebElement] = [],
    ) -> None:
        """Answer each question.

        Args:
            question_number (str)                           : Question number in the form.
            answer_data (Dict[str,Dict[str,Any]], optional) : Answer collection for each question. Defaults to ``{}``.
            inputElements (List[WebElement], optional)      : List of input elements in the form. Defaults to ``[]``.
        """
        answer = answer_data.get(str(question_number), {})
        no = int(answer.get("no", 1))
        val = answer.get("val", "")

        target: WebElement = inputElements[no - 1]
        question_type: str = target.get_attribute("type")
        if question_type == "radio":
            target.click()
        elif question_type == "checkbox":
            for n in set(val):
                inputElements[int(n) - 1].click()
        elif question_type == "text":
            if not isinstance(val, str):
                val = ",".join(val)
            target.send_keys(val)

    def login(
        self, driver: WebDriver, url: str, login_data: Dict[str, Dict[str, str]] = {}
    ) -> None:
        """Perform the login procedure required to answer the form.

        Args:
            driver (WebDriver): [description]
            url (str): [description]
            login_data (Dict[str,Dict[str,str]], optional) : [description]. Defaults to ``{}``.
        """
        self.print("[START LOGIN]")
        driver.get(url)
        login_data = copy.deepcopy(sorted(login_data.items(), key=lambda x: x[0]))
        for no, values in login_data:
            {"click": try_find_element_click, "send_keys": try_find_element_send_keys,}[
                values.pop("func")
            ](driver=driver, verbose=self.verbose, **values)
        self.print("[END LOGIN]")

    def run(self, **kwargs) -> None:
        """Login and Answer the forms."""
        with get_chrome_driver() as driver:
            self.login(
                driver=driver,
                url=self.data["URL"],
                login_data=self.data.get("login", {}),
            )
            self.answer_form(driver=driver, **kwargs)

    def answer_form(self, driver: WebDriver, **kwargs) -> None:
        """Answer the forms.

        Args:
            driver (WebDriver): An instance of Selenium WebDriver.
        """
        self.print("[START ANSWERING FORM]")
        answer_data = self.data.get("answer", {})
        answered_question_numbers = []
        not_found_count = 0
        self.print("[START FORM]")
        while True:
            visible_questions = driver.find_elements_by_class_name(
                name="office-form-question"
            )
            if len(answered_question_numbers) == 0:
                if not_found_count > 5:
                    break
                time.sleep(1)
                not_found_count += 1
            elif len(answered_question_numbers) == len(visible_questions):
                break
            for question in visible_questions:
                # NOTE: question number depends on forms.
                question_number = int(
                    question.find_element_by_css_selector(
                        "span.ordinal-number"
                    ).text.rstrip(".")
                )
                if question_number not in answered_question_numbers:
                    self.print(
                        question.find_element_by_css_selector(
                            "div.question-title-box"
                        ).text
                        + "\n"
                    )
                    inputElements = question.find_elements_by_tag_name(name="input")
                    num_inputElements = len(inputElements)
                    for j, inputTag in enumerate(inputElements):
                        question_type = inputTag.get_attribute("type")
                        value = inputTag.get_attribute("value")
                        # NOTE: input no is 1-based index.
                        self.print(
                            f"\t{j+1:>0{len(str(num_inputElements))}} [{question_type}] {value}"
                        )
                    self.answer_question(
                        question_number=str(question_number),
                        answer_data=answer_data,
                        inputElements=inputElements,
                    )
                    answered_question_numbers.append(question_number)
                    self.print("-" * 30)
        self.print("[END FORM]")
        try_find_element_click(
            driver=driver,
            by="css selector",
            identifier="button.__submit-button__",
            verbose=self.verbose,
        )
        self.print("[END ANSWERING FORM]")
