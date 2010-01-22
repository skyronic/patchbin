// Comments javascript file



function main()
{
	// Register all the valid lines for commentary
	if(typeof(console) == "undefined") // No firebug :(
	{
		console = {
log:function(string, args, args)
	{
		// Do nothing
	}
		};
	}
	$("td.whiteback").bind("dblclick", drawCommentForm);
	$("td.redback").bind("dblclick", drawCommentForm);
	$("td.greenback").bind("dblclick", drawCommentForm);
	// addCommentToDiffLine('lhs', '2', '75', '1', 'Anirudh', "Hey There!");
    LoadComments();
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
	commentContent = $(this.parentNode).siblings("pre.commentContent")[0].innerHTML;
	commentAuthor = $(this.parentNode).siblings("p.commentAuthor")[0].innerHTML;

	replyString = "";
	commentLines = commentContent.split('\n');
	for(commentindex in commentLines)
	{
		replyString += "> " + commentLines[commentindex] + "\n";
	}
	commentFormAtDiv(targetCell, replyString);
}


/*
 * Adds a comment to the diff line in the table when the side,
 * and the line number, etc are specified. This is prolly going
 * to be useful when the server knows only the side, chunk, line, etc
 * and spits out the parameters into the javascript.
 */
function addCommentToDiffLine(side, chunkNum, line, commentIndex, author, content)
{
	idString = diffLineIdFromParams(side, chunkNum, line);
	if(idString != "error")
	{
		addCommentToDiffElement(idString, commentIndex, author, content);
	}
}

/*
 * Adds the actual div into the DOM. Extracted from addCommentToDiffLine.
 */
function addCommentToDiffElement(id, commentIndex, author, content)
{
	idString = id;
	if(idString != "error")
	{
		commentDiv = document.createElement("div");
		commentDiv.innerHTML = '<div class="commentText"><p class="commentAuthor">'
			+ author + ' Said:</p><pre class="commentContent">' + content +
			'</pre><p>[<a href="#">Reply</a>]</p></div>';

		appendDivToDiffLine(idString, commentDiv);

		$(commentDiv).find("a").bind("click", {commentElement:commentDiv}, replyToComment);
	}
}

/*
 * Gets a valid ID from the parameters
 */
function diffLineIdFromParams(side, chunkNum, line)
{
	idString = side + "-" + chunkNum + "-" + line;
	if(document.getElementById(idString))
		return idString;
	return "error";
}

function elementParamsFromDiffId(idString)
{
    // Check validity from id String
    if(idString.match(/^(lhs|rhs){1}-\d{1,3}-\d{1,4}$/))
    {
        components = idString.split('-');
        var params = { side:components[0], chunk:components[1], line:components[2]};
        return params;
    }
    else
    {
        return null;
    }
}

/*
 * Sends the XHR Request to the server and also handles the response.
 *
 */
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
        submitButton = this;

		// Do an AJAX POST request to the current URL + newcomment
		// neat trick to extract everything before the hashtag
		currentUrl = document.location.href.split("#")[0];
		postURL = currentUrl + "/newcomment";

        var diffElement = $(commentDiv).parents("td")[0];

        // Get the parameters of the element
        elemParams = elementParamsFromDiffId(diffElement.id);
        if(elemParams!=null)
        {

        var POSTData = {
name:commentName ,message:commentString,side:elemParams.side,
     chunk:elemParams.chunk, line:elemParams.line
				};
        
		$.post(postURL, POSTData,
				 function(data)
				{
					console.log("Recieved data: ", data);

					if(data == "OK")
					{
						// first, remove the comment div:
						$(commentDiv).hide();

                        // TODO: Change the value of comment ID
                        addCommentToDiffElement(diffElement.id, 0, commentName, commentString);
					}
					else if(data == "ERROR")
					{
						alert("Something went wrong with saving your comment. Please try again later");
                        submitButton.disabled = false;
					}
				});
        }
	else
	{
	 console.log('elemparams is null, uh oh');
	}
	}
}

/*
 *
 */
function commentFormAtDiv(element, content)
{
	commentFormDiv = document.createElement("div");
	commentID = 0;
	commentFormDiv.id = element.id + "-comment-" + commentID;
	commentFormDiv.innerHTML = '<div id="" class=""><p>Name: <input type="text" id="" /></p><p><textarea>' + content + '</textarea></p><p><button>Submit!</button></div>';
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
	if($(this).hasClass("comentform") || $(this).hasClass("commentText"))
	{
		// ignore
	}
	else
	{
		commentFormAtDiv(this, "");
	}
}

$(document).ready(main);
