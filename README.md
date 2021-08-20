# Form Auto Fill In

<a href="https://github.com/iwasakishuto/Form-Auto-Fill-In"><img src="https://iwasakishuto.github.io/Form-Auto-Fill-In/images/site/header.png" alt="header"></a>
<a href="https://github.com/iwasakishuto/Form-Auto-Fill-In"><img src="https://badge.fury.io/gh/iwasakishuto%2FForm-Auto-Fill-In.svg" alt="GitHub Version"></a>
<a href="https://github.com/iwasakishuto/Form-Auto-Fill-In/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000" alt="License"></a>
<br/>
<a href="https://github.com/iwasakishuto/Form-Auto-Fill-In/blob/master/.github/workflows/UHMRF.yml"><img src="https://github.com/iwasakishuto/Form-Auto-Fill-In/workflows/Answer%20UTokyo%20Health%20Management%20Report%20Form/badge.svg" alt="Answer UTokyo Health Management Report Form"></a>
<a href="https://youtu.be/A_1zfeCDN24"><img src="https://img.shields.io/badge/YouTube-FF0000?style=flat-square&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://github.com/iwasakishuto/Form-Auto-Fill-In/wiki/100.-%E6%9D%B1%E4%BA%AC%E5%A4%A7%E5%AD%A6-%E5%81%A5%E5%BA%B7%E7%AE%A1%E7%90%86%E5%A0%B1%E5%91%8A%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0"><img src="https://img.shields.io/badge/Documentation-Japanese-ff0000?style=flat-square" alt="Japanese Documentation"></a>
<a href="https://iwasakishuto.github.io/Form-Auto-Fill-In/UTokyo_Health_Management_Report_Form.html"><img src="https://img.shields.io/badge/Documentation-English-0000ff?style=flat-square" alt="English Documentation"></a>

Answer Form Automatically.

## Supported Forms

Currently, the following forms are supported:

|                                              [UTokyo Health Management Report Form](https://www.u-tokyo.ac.jp/covid-19/ja/safety/healthcheck.html)                                               |                                                                                                   |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------: |
| [![The University of Tokyo](https://iwasakishuto.github.io/Form-Auto-Fill-In/images/UHMRF/logo.png)](https://iwasakishuto.github.io/Form-Auto-Fill-In/UTokyo_Health_Management_Report_Form.html) | ![Juntendo University](https://iwasakishuto.github.io/Form-Auto-Fill-In/images/juntendo/logo.png) |

## How to use?

The program can be executed by the following two methods, but the former is recommended.

### 1. Automatic Execution with Github Actions (recommended)

Look at the [documentation](https://iwasakishuto.github.io/Form-Auto-Fill-In/) or YouTube (for UTokyo Health Management Report Form) below:

[![UHMRF thumbnail](https://iwasakishuto.github.io/Form-Auto-Fill-In/images/UHMRF/thumbnail.png)](https://youtu.be/A_1zfeCDN24)

### 2. Install in your Local Env

You can also install it in your own environment and run it as appropriate.

#### Installation

Build the environment with [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://github.com/python-poetry/poetry).

```sh
$ git clone https://github.com/iwasakishuto/Form-Auto-Fill-In.git
$ cd Form-Auto-Fill-In
$ pyenv install 3.8.9
$ pyenv local 3.8.9
$ python -V
Python 3.8.9
$ poetry install
```

#### Run (ex.UHMRF)

Execute the following command on terminal. (command prompt)

```sh
$ poetry run answer-UHMRF -P "UHMRF_PLACE=<PLACE>" \
                          -P "UTOKYO_ACCOUNT_MAIL_ADDRESS=<ADDRESS>" \
                          -P "UTOKYO_ACCOUNT_PASSWORD=<PASSWORD>"
[START LOGIN]
Succeeded to locate element with xpath=//input[@type='email']
Succeeded to fill <ADDRESS> in element with xpath=//input[@type='email']
Succeeded to locate element with xpath=//input[@type='submit']
Succeeded to click the element with xpath=//input[@type='submit']
Succeeded to locate element with id=passwordInput
Succeeded to fill <PASSWORD> in element with id=passwordInput
Succeeded to locate element with id=submitButton
Succeeded to click the element with id=submitButton
Succeeded to locate element with xpath=//input[@type='submit']
Succeeded to click the element with xpath=//input[@type='submit']
[END LOGIN]
[START ANSWERING FORM]
[START 0th PAGE]
1.
Vaccination in the event of a cancellation
In the event of a sudden cancellation, we may contact those interested in getting vaccinated for an appointment. Would you be willing/able to arrive at the vaccination site (Sanjo Conference Hall on the Hongo Campus) within 30 minutes of being contacted?

	1 [radio] 希望しない
	2 [radio] 希望する（到着可能、かつ、そのような形でも接種を受けたい）
------------------------------
Succeeded to locate element with css selector=button.section-next-button
Succeeded to click the element with css selector=button.section-next-button
[END 0th PAGE]
[START 1th PAGE]
2.
Email address
【ECCSクラウドメール(共通ID@g.ecc.u-tokyo.ac.jp)宛の送信にはアドレスの入力は不要です。その他のアドレスへの送信を希望する場合はメールアドレスを入力してください。UTokyoアカウント[共通ID@utac.u-tokyo.ac.jp] はメールアドレスではありませんのでご注意ください）】
※ECCSクラウドメールを利用したことがない方は下記URLからアカウント利用の初期設定をしてください（初期設定時のパスワード変更には最大1時間かかります）。 https://hwb.ecc.u-tokyo.ac.jp/wp/literacy/email/initialize/

	1 [radio] ECCSクラウドメール(共通ID@g.ecc.u-tokyo.ac.jp)宛に送信
	2 [radio] on
	3 [text]
------------------------------
3.
Campus entry
[Check the campus(es) you are going to enter today (where applicable).]

	1 [checkbox] 本郷地区／Hongo Area
	2 [checkbox] 駒場Ⅱ地区／KomabaⅡ Area
	3 [checkbox] 柏地区／Kashiwa Area
	4 [checkbox] その他／Other Campus
------------------------------
4.
Main place(s) you will be staying at or visiting on campus today
Please enter the name(s) and floor(s) of the building(s) you will be staying at or visiting as listed on the campus map on the UTokyo website ( https://www.u-tokyo.ac.jp/en/about/access.html ).

	1 [text]
------------------------------
5.
Body temperature (morning)

	1 [radio] 37.0度未満／Less than 37.0 degrees Celsius
	2 [radio] 37.0度以上37.5度未満／Less than 37.5 degrees Celsius
	3 [radio] 37.5度以上／37.5 degrees Celsius or more
------------------------------
6.
Presence or absence of symptoms
Please answer regarding the presence of symptoms today and during the past week.
If you select "Yes", please answer in detail about the presence or absence of individual symptoms.

(1) Recent breathing difficulties:
heavy breathing (respiratory rate increased), sudden breathing difficulty, short of breath when you move a little, chest pain, not able to breathe unless you sit down or lie down, gasping for breath, or wheezing
(2) Recent taste and smell disorders (no sense of smell or taste)
(3) Recent coughing and sputum/phlegm (severe cough or sputum/phlegm)
(4) Recent general malaise
(5) Nausea
(6) Diarrhea
(7) Others:
no appetite, nasal discharge, nasal congestion, sore throat, headache, joint pain, muscle pain, poor condition all day, body rash, red eye, a large amount of eye discharge, etc.

	1 [radio] はい／Yes
	2 [radio] いいえ／No
------------------------------
Succeeded to locate element with css selector=button.__submit-button__
Succeeded to click the element with css selector=button.__submit-button__
[END 1th PAGE]
[END ANSWERING FORM]
```
