import os
import re
import secrets
import sys
from hashlib import md5
from textwrap import dedent
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

import feedparser
from IPython import display


__all__ = [
    "Video",
    "Checkboxes",
    "MultipleChoice",
]


def _add_solution(el, text):
    """Add a solution xml to a problem."""
    sol = SubElement(el, "solution")
    div = SubElement(sol, "div")
    div.attrib["class"] = "detailed-solution"
    title = SubElement(div, "p")
    title.text = "Explanation"
    content = SubElement(div, "p")
    content.text = text


def _replace_latex_delimiters(text):
    return re.sub(r"\$(.+?)\$", (lambda match: fr"\({match.group(1)}\)"), text)


class Video(display.YouTubeVideo):
    def __init__(
        self,
        id,
    ):
        super().__init__(id, rel=0, cc_load_policy=1)

    def _repr_html_(self):
        orig = super()._repr_html_()
        return '<div class="embed-responsive embed-responsive-16by9">{}</div>'.format(
            orig.replace("<iframe", '<iframe class="embed-responsive-item" ')
        )


class Checkboxes:
    def __init__(
        self,
        question,
        answers,
        correct_answers,
        explanation=None,
    ):
        """
        A checkboxes html component

        input types
        -----------

        question : string
        answers : list of strings
        correct_answers : list of int

        """
        self.question = question
        self.answers = answers
        self.correct_answers = correct_answers
        self.explanation = explanation

    def _repr_html_(self):
        s = "<h4>%s</h4>" % self.question
        s += '<form><input type="checkbox">  '
        s += '<br><input type="checkbox">  '.join(self.answers)
        s += "</form>"

        answer = "The correct answer{}:<br>".format(
            "s are" if len(self.correct_answers) > 1 else " is"
        )
        tmp = []
        for i in self.correct_answers:
            tmp.append(self.answers[i])
        answer += ", ".join(t for t in tmp)
        answer += "."
        if self.explanation is not None:
            answer += "<br><i>" + self.explanation + "</i>"

        s += dedent(
            """
        <button title="Click to show/hide content" type="button"
        onclick="if(document.getElementById('{0}')
         .style.display=='none') {{document.getElementById('{0}')
         .style.display=''}}else{{document.getElementById('{0}')
         .style.display='none'}}">Show answer</button>

        <div id="{0}" style="display:none">
        {1} <br>
        </div>    """
        )
        return s.format(secrets.token_urlsafe(20), answer)


class MultipleChoice:
    def __init__(
        self,
        question,
        answers,
        correct_answer,
        explanation=None,
    ):
        """
        Multiple choice question html component

        Parameters:
        -----------

        question : string
        answers : list of strings
        correct_answers : int

        """
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.explanation = explanation

    def _repr_html_(self):
        s = "<h4>%s</h4>" % self.question
        s += "<form>"
        for ans in self.answers:
            s += f'<input type="radio" name="answer" value="{ans}">{ans}<br>'
        s += "</form>"

        answer = "The correct answer is: <br>"
        answer += self.answers[self.correct_answer]
        if self.explanation is not None:
            answer += f"<br><i>" + self.explanation + "</i>"

        s += dedent(
            """
        <button title="Click to show/hide content" type="button"
        onclick="if(document.getElementById('{0}')
         .style.display=='none') {{document.getElementById('{0}')
         .style.display=''}}else{{document.getElementById('{0}')
         .style.display='none'}}">Show answer</button>

        <div id="{0}" style="display:none">{1}</div>"""
        )
        return s.format(secrets.token_urlsafe(20), answer)
