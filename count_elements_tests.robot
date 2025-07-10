*** Settings ***
Library    SeleniumLibrary    timeout=10

*** Variables ***
${URL}                https://github.com/PS-RANASINGHE/Test-Repo-for-Home-DIYs
${CODE_BTN}           xpath=//button[normalize-space(.//span[@data-component='text'])='Code']
${CODE_TABLE}         xpath=//*[@id="__primerPortalRoot__"]//div[contains(@class,'Box')]
${MAP_IFRAME}         xpath=//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[3]/div[2]/div/div[2]/article/section[2]
${VIDEO}              xpath=//video
${MAIN_BTN}           xpath=//*[@id="repo-content-pjax-container"]/div/div/div/div[1]/react-partial/div/div/div[2]/div[1]/div[1]
${INTRO}              xpath=//*[@id="repo-content-pjax-container"]//article/ul[1]/li[1]/a
${INTRO_SECTION}      user-content-introduction
${HREF_LNK}           xpath=//a[normalize-space(.)='Terms']
${EXPECTED}           https://docs.github.com/en/site-policy/github-terms/github-terms-of-service


*** Keywords ***
Video Should Be Playing
    [Arguments]    ${locator}
    [Documentation]    Fails unless the video has advanced and isn’t paused or ended
    ${playing}=    Execute Javascript
    ...    return document.querySelector('video').currentTime > 0
    ...      && !document.querySelector('video').paused
    ...      && !document.querySelector('video').ended;
    Should Be True    ${playing}    Video at '${locator}' is not playing

*** Test Cases ***
Click Code, Pan Map And Play Video
    Open Browser    ${URL}    Chrome
    Maximize Browser Window
    Set Selenium Speed    0.3s

Click the Code panel
    Wait Until Element Is Visible    ${CODE_BTN}
    Click Element                    ${CODE_BTN}
    Wait Until Element Is Visible    ${CODE_TABLE}
    Click Element                    ${CODE_BTN}

Pan the GeoJSON map by dragging the iframe
    Wait Until Element Is Visible    ${MAP_IFRAME}
    Drag And Drop By Offset          ${MAP_IFRAME}    150    0
    Sleep                            9s
    Drag And Drop By Offset          ${MAP_IFRAME}   -150    0

Click the video element to start playback
    Wait Until Element Is Visible    ${VIDEO}
    Click Element                    ${VIDEO}

     # 1) Reveal & click the video
    Wait Until Element Is Visible    ${VIDEO}
    #Click Element                    ${VIDEO}

    # 2) Wait up to 10s, polling every 1s, until it actually plays
    Wait Until Keyword Succeeds    10s    1s    Video Should Be Playing    ${VIDEO}

    # - Testing a main button whether the click function work -
    Wait Until Element Is Visible    ${MAIN_BTN}
    Click Element                    ${MAIN_BTN}
    Wait Until Element is Visible    xpath =//*[@id="selectPanel"]
    Click ELement                    ${MAIN_BTN}


    # -Testing a href link whether it directs to the correct location -
Verify “Introduction” Anchor Link
    [Documentation]    Clicks the “Introduction” link and verifies the fragment
    Wait Until Element Is Visible    ${INTRO}
    Click Element                    ${INTRO}

    ${current}=    Get Location
    Should Contain    ${current}    \#introduction    URL did not update

    # Now scroll the GitHub‐generated anchor into view by supplying id=…
    Scroll Element Into View         id=${INTRO_SECTION}
    Wait Until Element Is Visible    id=${INTRO_SECTION}

    ${in_view}=    Execute Javascript
    ...    var el=document.getElementById('${INTRO_SECTION}');
    ...    var r=el.getBoundingClientRect();
    ...    return r.top>=0 && r.bottom<=window.innerHeight;
    Should Be True    ${in_view}    Section is not scrolled into view


Check Hyperlink and Open a New window in browser

     Wait Until Element Is Visible      ${HREF_LNK}
     Click Element                      ${HREF_LNK}
     Wait Until Location Contains       ${EXPECTED}    10s
     Location Should Be                 ${EXPECTED}

    [Teardown]    Close Browser