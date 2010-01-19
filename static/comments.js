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
	var targetCell = $(this).parents("td")[0];
	console.log("Target cell is: ", targetCell);
	commentFormAtDiv(targetCell);

}

function addCommentToDiffLine(side, chunkNum, line, commentIndex, author, content)
{
	idString = diffLineIdFromParams(side, chunkNum, line);
	if(idString != "error")
	{
		commentDiv = document.createElement("div");
		commentDiv.innerHTML = '<div class="commentText"><p class="commentAuthor">'
			+ author + ' Said:</p><p class="commentContent">' + content +
			'</p><p>[<a href="#">Reply</a>]</p></div>';

		appendDivToDiffLine(idString, commentDiv);

		$(commentDiv).find("a").bind("click", {commentElement:commentDiv}, replyToComment);
	}
}

function addCommentToDiffElement(id, author, content)
{
	idString = diffLineIdFromParams(side, chunkNum, line);
	if(idString != "error")
	{
		commentDiv = document.createElement("div");
		commentDiv.innerHTML = '<div class="commentText"><p class="commentAuthor">'
			+ author + ' Said:</p><p class="commentContent">' + content +
			'</p><p>[<a href="#">Reply</a>]</p></div>';

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

		// Disable the button
		this.disabled = true;

		// Do an AJAX POST request to the current URL + newcomment
		// neat trick to extract everything before the hashtag
		currentUrl = document.location.href.split("#")[0];
		postURL = currentUrl + "/newcomment";

		$.post(postURL,
				{
					name:commentName ,message:commentString,
				}, function(data)
				{
					console.log("Recieved data: ", data);

					if(data == "OK")
					{
						// first, remove the comment div:
						$(commentDiv).hide();
					}
					else if(data == "ERROR")
					{
						alert("Something went wrong with saving your comment. Please try again later");
					}
				});
	}
}

function commentFormAtDiv(element)
{
	commentFormDiv = document.createElement("div");
	commentID = 0;
	commentFormDiv.id = element.id + "-comment-" + commentID;
	commentFormDiv.innerHTML = '<div id="" class=""><p>Name: <input type="text" id="" /></p><p><textarea></textarea></p><p><button>Submit!</button></div>';
	$(commentFormDiv).addClass("commentform");

	if($(commentFormDiv).hasClass("whiteback"))
		$(commentFormDiv).removeClass("whiteback");
	if($(commentFormDiv).hasClass("greenback"))
		$(commentFormDiv).removeClass("greenback");
	if($(commentFormDiv).hasClass("redback"))
		$(commentFormDiv).removeClass("redback");

	appendDivToDiffLine(element.id, commentFormDiv);

	// Find the submit button and hook to the click event
	$(element).find('button').bind('click', {commentDiv:commentFormDiv}, postCommentFromForm);

}

function drawCommentForm (e)
{
	console.log('Drawing comment form');
	console.log(e);
	console.log(this);

	commentFormAtDiv(this);
	//$(this.parentNode).after("<tr><th></th><td>hi there</td><th></th><td></td></tr>");
}

$(document).ready(main);