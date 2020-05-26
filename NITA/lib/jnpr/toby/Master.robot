*** Settings ***
Documentation  Master Resource file for Toby
...            This resource file is collection of all resource files defined
...            in Toby

Library     /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/engines/config/config.py
Library     /Users/srigupta/Desktop/git/filr/Nita/lib/jnpr/toby/engines/monitor/MonitoringEngine.py
Library     /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/engines/macro/cmd_macro.py
Library     /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/engines/events/eventEngine.py
Library     /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/utils/parallel.py
Library     /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/logger/logger.py
Resource    /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/engines/verification/verification.robot
Resource    /Users/srigupta/Desktop/git/file/Nita/lib/jnpr/toby/toby.robot
*** Keywords ***
