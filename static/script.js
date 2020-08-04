function sendRequest(event)
{
	event.preventDefault();
	var formData = new FormData(form);
	if (((formData.get('fileLink') == '') && (formData.get('fileLocal')) == '') || ((formData.get('fileLink') != '') && (formData.get('fileLocal') != '')))
	{
		alert("Предупреждение: заполните только одно из полей!");
	}
	else
	{
		form.submit();
	}
}
var form1 = document.forms.SendImage.addEventListener('submit', sendRequest);
var form = document.forms.SendImage