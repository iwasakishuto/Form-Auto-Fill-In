# coding: utf-8
import copy
import time
from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Callable, Dict, List, Optional, Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..utils._colorings import toACCENT, toBLUE, toGREEN
from ..utils._path import canonicalize_path
from ..utils.driver_utils import get_chrome_driver, try_find_element_func
from ..utils.generic_utils import load_data, wrap_end, wrap_start


class BaseForm(ABC):
    """Abstract Basement Class for Answering Form Automatically.

    Args:
        path (str)                              : Path to json data that describes the procedure of form.
        secrets_dict (Dict[str, str], optional) : Key and value pairs defined in github secrets. It is used because the password etc. is not output as it is. Defaults to ``{}``.
        verbose (bool, optional)                : Whether to print message or not. Defaults to ``True``.

    Attributes:
        verbose (bool)                      : Whether to print message or not. Defaults to ``True``.
        print (Callable[[Any], type(None)]) : Print function according to ``verbose``
        data (Dict[str, Any])               : Data that describes the procedure of form.
        secrets_dict (Dict[str, str])       :
        path (str)                          : Path to json data that describes the procedure of form.
    """

    def __init__(
        self,
        path: str,
        secrets_dict: Dict[str, str] = {},
        verbose: bool = True,
        **kwargs,
    ):
        self.verbose: bool = verbose
        self.print: Callable[[Any], type(None)] = print if verbose else lambda *args: None
        self.data: Dict[str, Any] = load_data(canonicalize_path(path))
        self.secrets_dict: Dict[str, str] = secrets_dict
        self.path: str = path

    # <--- Useful Methods ---
    def decode_secrets(self, string: Union[str, List[str]]) -> str:
        """Convert from the identifier of Github Secrets to Decoded Raw string.

        Args:
            string (Union[str, List[str]]) : String or List of Strings.

        Returns:
            str: Decoded raw string.
        """
        if isinstance(string, str):
            string = [string]
        return ",".join([self.secrets_dict.get(e, e) for e in string])

    def check_labels(
        self,
        labels: List[WebElement],
        checks: List[int],
    ):
        num_labels: int = len(labels)
        digit: int = len(str(num_labels))

        for i, label in enumerate(labels, start=1):
            mark: str = " "
            if i in checks or str(i) in checks:
                label.click()
                mark = "x"
            self.print(f"\t{i:>0{digit}}/{num_labels} [{mark}] {self.get_label_text(label)}")

    def input_answer(self, msg: str = "Your Answer{isMultiple}", isMultiple=False) -> Any:
        fmtkwargs: Dict[str, str] = {}
        if "{isMultiple}" in msg:
            fmtkwargs.update(
                {
                    "isMultiple": " (Multiple inputs are possible by dividing with ',')"
                    if isMultiple
                    else ""
                }
            )

        ans = input("> " + msg.format(**fmtkwargs) + ": ")

        if isMultiple:
            ans = [e.strip() for e in ans.split(",")]
        return ans

    # --- Useful Methods --->

    # <--- Main Methods ---
    def run(self, browser: bool = False, **kwargs) -> None:
        """Login and Answer the forms.

        Args:
            browser (bool, optional) : Whether you want to run Chrome with GUI browser. Defaults to ``False``.
        """
        with get_chrome_driver(browser=browser) as driver:
            self.login(driver=driver)
            self.answer_form(driver=driver, **kwargs)
            self.logout(driver=driver)

    def login(self, driver: WebDriver) -> None:
        """Perform the login procedure required to answer the form.

        Args:
            driver (WebDriver): [description]
        """
        url: str = self.data.get("URL")
        if url is not None:
            self.print(f"Visit Form: {toBLUE(url)}")
            driver.get(url)
            self.print(wrap_start("START LOGIN"))
            for loginkwargs in self.data.get("login", []):
                _loginkwargs = loginkwargs.copy()
                func = _loginkwargs.pop("func")
                try_find_element_func(
                    driver=driver,
                    funcname=loginkwargs.pop("func"),
                    secrets_dict=self.secrets_dict,
                    verbose=self.verbose,
                    **_loginkwargs,
                )
            self.print(wrap_end("END LOGIN"))

    def answer_form(self, driver: WebDriver, deque_maxlen: int = 3, **kwargs) -> None:
        """Answer the forms.

        Args:
            driver (WebDriver): An instance of Selenium WebDriver.
        """
        self.print(wrap_start("START ANSWERING FORM"))
        self.print(toACCENT("[TITLE]") + f"\n{self.find_form_title(driver=driver)}\n")
        for i, ith_answer_data in enumerate(self.data.get("answer", [{}])):
            self.print(wrap_start(f"START {i}th PAGE", indent=4))
            answered_question_identifiers: List[str] = []
            num_visible_questions = deque([-1] * deque_maxlen, maxlen=deque_maxlen)
            # num_questions_to_answer: int = len([e for e in ith_answer_data.keys() if e != "next"])

            while True:
                time.sleep(1)
                visible_questions = self.find_visible_questions(driver=driver)
                num_visible_questions.append(visible_questions)

                # STOP CONDITION
                # if len(answered_question_identifiers) >= num_questions_to_answer or
                if all([num_visible_questions[0] == e for e in list(num_visible_questions)[1:]]):
                    break

                for question in visible_questions:
                    question_identifier = self.find_question_identifier(
                        driver=driver, question=question
                    )
                    if question_identifier not in answered_question_identifiers:
                        self.print(
                            toACCENT(f'[KEY: "{question_identifier}"]\n')
                            + f"{self.find_question_title(driver=driver, question=question)}\n"
                        )
                        self.answer_question(
                            question=question,
                            answer=ith_answer_data.get(question_identifier, {}),
                        )
                        answered_question_identifiers.append(question_identifier)
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
            self.print(wrap_end(f"END {i}th PAGE", indent=4))
        self.print(wrap_end("END ANSWERING FORM"))

    def logout(self, driver: WebDriver) -> None:
        """Perform the login procedure required to answer the form.

        Args:
            driver (WebDriver): [description]
        """
        self.print(toACCENT("[END]"))

    # --- Main Methods --->

    # <--- Abstract Methods (NOTE: When inheriting this class, you need to change these methods.) ---
    @abstractmethod
    def find_form_title(self, driver: WebDriver) -> str:
        return ""

    @abstractmethod
    def get_label_text(self, label: WebElement) -> str:
        return "text"

    @abstractmethod
    def find_visible_questions(self, driver: WebDriver) -> List[WebElement]:
        return []

    @abstractmethod
    def find_question_identifier(self, driver: WebDriver, question: WebElement) -> str:
        return ""

    @abstractmethod
    def find_question_title(self, driver: WebDriver, question: WebElement) -> str:
        return ""

    @abstractmethod
    def answer_on_demand(self, question: WebElement) -> Dict[str, Any]:
        labels: List[WebElement] = question.find_elements_by_tag_name(name="label")
        if len(labels) > 0:
            self.check_labels(labels=labels, checks=[])

        val = self.input_answer(isMultiple=len(labels) > 0)

        return {"val": val}

    @abstractmethod
    def answer_question(
        self,
        question: WebElement,
        answer: Dict[str, Any] = {},
    ) -> None:
        """Answer each question.

        Args:
            question_identifier (str)                           : Question number in the form.
            answer_data (Dict[str,Dict[str,Any]], optional) : Answer collection for each question. Defaults to ``{}``.
            inputElements (List[WebElement], optional)      : List of input elements in the form. Defaults to ``[]``.
        """
        if "key" not in answer:
            answer.update(self.answer_on_demand(question=question))

        print("Answer the Question :)")

    # --- Abstract Methods (NOTE: When inheriting this class, you need to change these methods.) --->
