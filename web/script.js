function enableTab(id) {
	var el = document.getElementById(id);
	el.onkeydown = function(e) {
		if (e.keyCode === 9) {
			var val = this.value,
			start = this.selectionStart,
			end = this.selectionEnd;

			this.value = val.substring(0, start) + '\t' + val.substring(end);
			this.selectionStart = this.selectionEnd = start + 1;

			return false;
		}
	};
}
enableTab('main-textarea');

document.getElementById('file-item').onclick = function () {
	var el = document.getElementById('file-wrapper-list');

	if (el.classList.contains('open-status')) {
		el.classList.remove('open-status');
	} else {
		el.classList.add('open-status');
	}
}

var isCtrl = false;
document.onkeyup=function(e){
	if(e.keyCode == 17) isCtrl=false;
}

document.onkeydown = function (e) {
	if(e.keyCode == 17) isCtrl=true;
	if(e.keyCode == 83 && isCtrl == true) {
		alert('ctrl+s');
		return false;
	} else if(e.keyCode == 79 && isCtrl == true) {
		create_file();
		alert('ctrl+o');
		return false;
	} else if(e.keyCode == 78 && isCtrl == true) {
		alert('ctrl+n');
		return false;
	}/* else if (e.keyCode == 116) {
		return false;
	}*/
}

function create_file() {
	var path = eel.create_file()(function (path) {
		alert(path);
	});
}