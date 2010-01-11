// Comments javascript file

function main()
{
	// Register all the valid lines for commentary
	$("td.whiteback").bind("dblclick", drawCommentForm);
	$("td.redback").bind("dblclick", drawCommentForm);
	$("td.greenback").bind("dblclick", drawCommentForm);

}

function drawCommentForm (e)
{
	console.log('Drawing comment form');
	console.log(e);
	console.log(this);
	

	$(this.parentNode).after("<tr><th></th><td>hi there</td><th></th><td></td></tr>");
}

$(document).ready(main);
