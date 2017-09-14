# -*- coding: utf-8 -*-
import subprocess, os

def call_powershell_timezone(timezone='-TimeZoneFriendlyName "West Pacific Standard Time"'):
    args = [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                                 '-ExecutionPolicy',
                                 'Unrestricted',
                                 './SetTimeZone.ps1',
                                 timezone]
    psxmlgen = subprocess.Popen(args, cwd=os.getcwd())
    result = psxmlgen.wait()


if __name__ == '__main__':
     call_powershell_timezone('-TimeZoneFriendlyName "West Pacific Standard Time"')
     call_powershell_timezone('-TimeZoneFriendlyName "China Standard Time"')

