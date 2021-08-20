# coding: utf-8
import copy
import time
from collections import deque
from typing import Any, Dict, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .utils import get_chrome_driver, load_data, try_find_element_func


class UtokyoHealthManagementReportForm:
    """If you want to create your own gateway class, please inherit this class.

    Args:
        path (str)                    : Path to json data that describes the procedure of form.
        secrets_dict (Dict[str, str]) : Key and value pairs defined in github secrets. It is used because the password etc. is not output as it is. Defaults to ``{}``.
        verbose (bool)                : Whether to print message or not. Defaults to ``True``.

    Attributes:
        verbose (bool)   : Whether to print message or not. Defaults to ``True``.
        print (callable) : Print function according to ``verbose``
        data (dict)      : Data that describes the procedure of form.
        path (str)       : Path to json data that describes the procedure of form.
    """

    def __init__(
        self,
        path: str,
        secrets_dict: Dict[str, str] = {},
        verbose: bool = True,
        **kwargs,
    ):
        self.verbose: bool = verbose
        self.print: callable = print if verbose else lambda *args: None
        self.data: Dict[str, Any] = load_data(path)
        self.secrets_dict = secrets_dict
        self.path: str = path

    @staticmethod
    def answer_question(
        question_number: str,
        answer_data: Dict[str, Dict[str, Any]] = {},
        inputElements: List[WebElement] = [],
        secrets_dict: Dict[str, str] = {},
    ) -> None:
        """Answer each question.

        Args:
            question_number (str)                           : Question number in the form.
            answer_data (Dict[str,Dict[str,Any]], optional) : Answer collection for each question. Defaults to ``{}``.
            inputElements (List[WebElement], optional)      : List of input elements in the form. Defaults to ``[]``.
            secrets_dict (Dict[str, str])                   : Key and value pairs defined in github secrets. It is used because the password etc. is not output as it is. Defaults to ``{}``.
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
                val = ",".join([secrets_dict.get(e, e) for e in val])
            else:
                val = secrets_dict.get(val, val)
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
            try_find_element_func(
                driver=driver,
                funcname=values.pop("func"),
                secrets_dict=self.secrets_dict,
                verbose=self.verbose,
                **values,
            )
        self.print("[END LOGIN]")

    def run(self, browser: bool = False, **kwargs) -> None:
        """Login and Answer the forms.

        Args:
            browser (bool, optional) : Whether you want to run Chrome with GUI browser. Defaults to ``False``.
        """
        with get_chrome_driver(browser=browser) as driver:
            self.login(
                driver=driver,
                url=self.data["URL"],
                login_data=self.data.get("login", {}),
            )
            self.answer_form(driver=driver, **kwargs)

    def answer_form(self, driver: WebDriver, deque_maxlen: int = 3, **kwargs) -> None:
        """Answer the forms.

        Args:
            driver (WebDriver): An instance of Selenium WebDriver.
        """
        self.print("[START ANSWERING FORM]")
        for i, ith_answer_data in enumerate(self.data.get("answer", [{}])):
            self.print(f"[START {i}th PAGE]")
            answered_question_numbers = []
            num_questions_to_answer = len(ith_answer_data) - 1
            num_visible_questions = deque([-1] * deque_maxlen, maxlen=deque_maxlen)
            while True:
                time.sleep(1)
                visible_questions = driver.find_elements_by_class_name(
                    name="office-form-question"
                )
                num_visible_questions.append(visible_questions)
                if all(
                    [
                        num_visible_questions[0] == e
                        for e in list(num_visible_questions)[1:]
                    ]
                ):
                    break
                elif len(answered_question_numbers) >= num_questions_to_answer:
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
                            answer_data=ith_answer_data,
                            inputElements=inputElements,
                            secrets_dict=self.secrets_dict,
                        )
                        answered_question_numbers.append(question_number)
                        self.print("-" * 30)
            next_data = ith_answer_data.get("next", {})
            if len(next_data) > 0:
                try_find_element_func(
                    driver=driver,
                    funcname=next_data.pop("func"),
                    secrets_dict=self.secrets_dict,
                    verbose=self.verbose,
                    **next_data,
                )
            self.print(f"[END {i}th PAGE]")
        self.print("[END ANSWERING FORM]")
