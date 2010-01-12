// Comments javascript file

function main()
{
	// Register all the valid lines for commentary
	$("td.whiteback").bind("dblclick", drawCommentForm);
	$("td.redback").bind("dblclick", drawCommentForm);
	$("td.greenback").bind("dblclick", drawCommentForm);
	addCommentToDiffLine('lhs', '2', '75', '1', 'Anirudh', "Hey There!");
}

function appendDivToDiffLine(id, contentDiv)
{
	// Do we need to do anything else?
	$("#" + id).append(contentDiv);
}

/**
 * Do not call. Triggered by jQuery
 */
function replyToComment(e)
{

}

function addCommentToDiffLine(side, chunkNum, line, commentIndex, author, content)
{
	idString = diffLineIdFromParams(side, chunkNum, line);
	if(idString != "error")
	{
		commentDiv = document.createElement("div");
		commentDiv.innerHTML = '<div class="commentText"><p class="commentAuthor">'
			+ author + ' Said:</p><p class="commentContent">' + content +
			'</p><p>[<a>Reply</a>]</p></div>';

		appendDivToDiffLine(idString, commentDiv);
		$(commentDiv).find("a").bind("click", {commentElement:commentDiv}, replyToComment);
	}
}

function diffLineIdFromParams(side, chunkNum, line)
{
	idString = side + "-" + chunkNum + "-" + line;
	if(document.getElementById(idString))
		return idString;
	return "error";
}
function postCommentFromForm(e)
{
	// get the container div
	if(typeof(e.data.commentDiv != "undefined"))
	{
		commentDiv = e.data.commentDiv;
		commentString = $(commentDiv).find('textarea')[0].value;
		commentName = $(commentDiv).find('input')[0].value;

		console.log(commentName + " wrote - " + commentString);
		this.disabled = true;
	}
}

function drawCommentForm (e)
{
	console.log('Drawing comment form');
	console.log(e);
	console.log(this);
	

	//$(this.parentNode).after("<tr><th></th><td>hi there</td><th></th><td></td></tr>");
	commentFormDiv = document.createElement("div");
	commentID = 0;
	commentFormDiv.id = this.id + "-comment-" + commentID;
	commentFormDiv.innerHTML = '<div id="" class=""><p>Name: <input type="text" id="" /></p><p><textarea></textarea></p><p><button>Submit!</button></div>';
	$(commentFormDiv).addClass("commentform");

	if($(commentFormDiv).hasClass("whiteback"))
		$(commentFormDiv).removeClass("whiteback");
	if($(commentFormDiv).hasClass("greenback"))
		$(commentFormDiv).removeClass("greenback");
	if($(commentFormDiv).hasClass("redback"))
		$(commentFormDiv).removeClass("redback");

	appendDivToDiffLine(this.id, commentFormDiv);

	// Find the submit button and hook to the click event
	$(this).find('button').bind('click', {commentDiv:commentFormDiv}, postCommentFromForm);
}

$(document).ready(main);
