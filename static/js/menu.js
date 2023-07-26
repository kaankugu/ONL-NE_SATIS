var width = 500;
var height = 400;
var popup;


function openPopup() {
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;

    // Pop-up'ın URL'sini dinamik olarak belirle
    var popupUrl = window.location.origin + "/logout";

    popup = window.open(popupUrl, "popup", "width=" + width + ",height=" + height + ",left=" + left + ",top=" + top);
    popup.focus();
}
