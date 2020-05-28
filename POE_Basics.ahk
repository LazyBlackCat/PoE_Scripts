#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

^!7:: 
    Run C:\Users\edhki\AppData\Local\Microsoft\WindowsApps\pythonw3.7.exe Autoclick_Highlighted_Stash.pyw
    Return
^!8:: 
    Run C:\Users\edhki\AppData\Local\Microsoft\WindowsApps\pythonw3.7.exe Auto_Chaos_Recipe.pyw
    Return
^!9:: 
    Run C:\Users\edhki\AppData\Local\Microsoft\WindowsApps\pythonw3.7.exe Find_Six_Sockets.pyw
    Return