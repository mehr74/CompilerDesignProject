function xmlToJson(xmlNode) {
    return {
        text: xmlNode.firstChild && xmlNode.firstChild.nodeType === 3 ? 
                  xmlNode.firstChild.textContent : '',
        children: [...xmlNode.children].map(childNode => xmlToJson(childNode))
    };
}

xhr = new XMLHttpRequest();
method = "GET";


function myFunction(xml) {
  	var xmlText = xml.responseXML;
  	console.log(xmlText);
  	console.log(xmlToJson(xmlText.documentElement));

	$('#data').jstree({
	    core: {
	      data: xmlToJson(xmlText.documentElement)
	    }
	});
}

function getXml() {
  xhr.open(method, "parse.xml", true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
    	myFunction(xhr);
    }
  };
  xhr.send();
}
getXml(); // start it 




