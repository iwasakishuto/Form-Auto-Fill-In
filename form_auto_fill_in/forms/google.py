# coding: utf-8
import copy
import re
import time
from collections import deque
from typing import Any, Callable, Dict, List, Optional, Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ..utils import get_chrome_driver, load_data, try_find_element, try_find_element_func
from .base import BaseForm


class GoogleForm(BaseForm):
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
        super().__init__(path=path, secrets_dict=secrets_dict, verbose=verbose, **kwargs)

    def find_form_title(self, driver: WebDriver) -> str:
        return driver.find_element_by_class_name("freebirdFormviewerViewHeaderHeaderBody").text

    def get_label_text(self, label: WebElement) -> str:
        return label.text

    def find_visible_questions(self, driver: WebDriver) -> List[WebElement]:
        return driver.find_elements_by_class_name(
            name="freebirdFormviewerViewNumberedItemContainer"
        )

    def find_question_identifier(self, driver: WebDriver, question: WebElement) -> str:
        return re.search(
            pattern=r"%\.@\.\[(\d+),",
            string=question.find_element_by_tag_name(name="div").get_attribute("data-params"),
        ).group(1)

    def find_question_title(self, driver: WebDriver, question: WebElement) -> str:
        return re.search(
            pattern=r'%\.@\.\[\d+,"(.+?)"',
            string=question.find_element_by_tag_name(name="div").get_attribute("data-params"),
        ).group(1)

    def answer_on_demand(self, question: WebElement) -> Dict[str, Any]:
        labels: List[WebElement] = question.find_elements_by_tag_name(name="label")
        if len(labels) > 0:
            self.check_labels(labels=labels, checks=[])

        val = self.input_answer(isMultiple=len(labels) > 0)

        return {"val": val}

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
            secrets_dict (Dict[str, str])                   : Key and value pairs defined in github secrets. It is used because the password etc. is not output as it is. Defaults to ``{}``.
        """
        if "val" not in answer:
            answer.update(self.answer_on_demand(question=question))

        labels: List[WebElement] = question.find_elements_by_tag_name(name="label")
        inputElements: List[WebElement] = question.find_elements_by_tag_name(name="input")

        if len(labels) > 0:
            # If other is selected and you are prompted for answering it.
            checks: List[Union[str, int]] = answer.get("val", [])
            self.check_labels(labels=labels, checks=checks)
            if len(inputElements) > 1:
                time.sleep(0.5)
                # Radio Button OR Check Box
                element = try_find_element(
                    driver=question,
                    by="class name",
                    identifier="freebirdFormviewerComponentsQuestionRadioOtherInputElement",
                    timeout=1,
                    verbose=False,
                ) or try_find_element(
                    driver=question,
                    by="class name",
                    identifier="freebirdFormviewerComponentsQuestionCheckboxOtherInputElement",
                    timeout=1,
                    verbose=False,
                )
                if element and "isFocused" in element.get_attribute(name="class"):
                    if "others" not in answer:
                        others = self.input_answer(msg="Your Answer for Others", isMultiple=False)
                    else:
                        others = answer["others"]
                    inputElements[1].send_keys(others)
        else:
            value: Union[str, List[str]] = answer.get("val", "")
            inputElements[0].send_keys(self.decode_secrets(value))
