/*$(document).ready(function() {*/
window.onload = function() {
	var editor = new CodeMirror.fromTextArea(document.getElementById("id_el_body"), {
	  width: "90%",
	  height: "500px",
	  theme: "cobalt",
	  lineWrapping: true,
	  path: "/static/",
	  mode: "text/html",
	  matchTags: {bothTags: true},
	  matchBrackets: true,
	  autoCloseTags: true,
	  extraKeys: {"Ctrl-J": "toMatchingTag",
        "Ctrl-W": function(cm) {
          cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Ctrl-E": function(cm) {
          if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        }}	,
	  content: document.getElementById("id_el_body").value
	});

	$("textarea#id_el_body + iframe").css("border", "1px solid rgb(204, 204, 204)");
};
