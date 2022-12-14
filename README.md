#Links

Создание HTML страницы со списком ссылок [links.html](links.html). Ссылка берётся из буфера обмена. Скрипт вызывается из контекстного меню проводника в папке, где нужно создать файл ссылок.

![context](img/r_mous.gif)

В разделе реестра **HKEY_CLASSES_ROOT\Directory\Background\Shell** добавляется подраздел, с командой, запускающей файл links.bat, который запускает скрипт.

![heestr](img/reg.gif)

###Окно добавления ссылки

![link](img/link.gif)

###Окно редактирования файла links.html

![edit](img/edit.gif)
