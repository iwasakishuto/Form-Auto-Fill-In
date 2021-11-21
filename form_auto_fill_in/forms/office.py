# coding: utf-8
import copy
import time
from collections import deque
from typing import Any, Dict, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..utils.driver_utils import get_chrome_driver, try_find_element_func, try_find_element_text
from ..utils.generic_utils import load_data
from .base import BaseForm


class OfficeForm(BaseForm):
    def __init__(
        self,
        path: str,
        secrets_dict: Dict[str, str] = {},
        verbose: bool = True,
        **kwargs,
    ):
        super().__init__(path=path, secrets_dict=secrets_dict, verbose=verbose, **kwargs)

    def find_form_title(self, driver: WebDriver) -> str:
        return try_find_element_text(
            driver=driver,
            by="class name",
            identifier="office-form-title-content",
            verbose=False,
            get_text=lambda e: e.text,
            default_text="TITLE",
        )

    def find_visible_questions(self, driver: WebDriver) -> List[WebElement]:
        return driver.find_elements_by_class_name(name="office-form-question")

    def find_question_identifier(self, driver: WebDriver, question: WebElement) -> str:
        return question.find_element_by_css_selector("span.ordinal-number").text.rstrip(".")

    def find_question_title(self, driver: WebDriver, question: WebElement) -> str:
        return question.find_element_by_css_selector("div.question-title-box").text

    def get_label_text(self, label: WebElement) -> str:
        return f"[{label.get_attribute('type')}] {label.get_attribute('value')}"

    def answer_on_demand(self, question: WebElement) -> Dict[str, Any]:
        inputElements: List[WebElement] = question.find_elements_by_tag_name(name="input")
        self.check_labels(labels=inputElements, checks=[])

        val = self.input_answer(isMultiple=len(inputElements) > 0)

        return {"no": val}

    def answer_question(
        self,
        question: WebElement,
        answer: Dict[str, Any] = {},
    ) -> None:
        """[summary]

        Args:
            question (WebElement)             : [description].
            answer (Dict[str, Any], optional) : [description]. Defaults to ``{}``.

        Kwargs:
            no
            text
        """

        if "no" not in answer:
            answer.update(self.answer_on_demand(question=question))

        numbers = answer.get("no", [])
        if not isinstance(numbers, (list, tuple)):
            numbers = [numbers]
        inputElements = question.find_elements_by_tag_name(name="input")
        self.check_labels(labels=inputElements, checks=numbers)

        for no in list(numbers):
            target: WebElement = inputElements[int(no) - 1]
            question_type: str = target.get_attribute("type")
            if question_type in ["radio", "checkbox"]:
                "Already Checked"
            if question_type == "text":
                if "text" not in answer:
                    text = self.input_answer(
                        msg=f"Your Text Answer for {self.get_label_text(target)}", isMultiple=False
                    )
                else:
                    text = answer["text"]
                target.send_keys(self.decode_secrets(text))
