Hi,

There are two files that you can choose both ways of treating the credential data.

First file is "lCloud.py" where the credentials have to be put at the top of the file, as instructed in the file.

To list files use command as:
python lCloud.py list

To upload file use command as:
python lCloud.py upload path_to_file s3_name

To regex filter use command as:
python lCloud.py list-filter regex

To delete by regex use command as:
python lCloud.py delete-filter regex



Second file is "lCloud_userInput.py" where the credentials like Bucketname and Prefix need to be updated on top, and then using the data credentials within commands.

To run the specific command use the command as above but add credential data as:

To list files use command as:
python lCloud.py access_key secret_key list

To upload file use command as:
python lCloud.py access_key secret_key upload path_to_file s3_name

To regex filter use command as:
python lCloud.py access_key secret_key list-filter regex

To delete by regex use command as:
python lCloud.py access_key secret_key delete-filter regex


Additionaly, there could be a third option, to use the encrypted for example yaml file, that the script will decrypt the file within the key and get the credentials to use within script.


Thank you for reading, in case of any questions please do not hesistate to contact me by email: jasiekaliszuk@gmail.com
Kind regards,
Jan Kaliszuk

