#!/usr/bin/python

import re
import string
from diff_match_patch import diff_match_patch
from core.models import Chunk, Comment, Patch

def split_into_chunks(patch):
    chunks = []
    # Split into lines
    lines = patch.split('\n')
    
    chunk = ''
    originalFile = ''
    newFile = ''
    chunkMode = False
    chunkStarted = False
    
    for line in lines:
        if(line == ''):
            continue
        if(line[0:3] == "---"):
            if(chunkMode):
                # Write the chunk
                currentChunk = (newFile, originalFile, chunk)
                chunks.append(currentChunk)
                chunk = ''
                newFile = ''
                originalFile = ''
            chunkMode = True
            originalFile = line
            chunkStarted = True
            continue
            
        if(line[0:3] == "+++"):
            if(not chunkStarted):
                continue
            chunkMode = True
            newFile = line
            continue
        
        if ('-+ '.find(line[0]) != -1):
            if(not chunkStarted):
                continue
            chunk = chunk + line
            chunk = chunk + '\n'
            continue
        
        if(line[0] == '@'):
            if(not chunkStarted):
                continue
  
            if(re.match('^@@.*@@$', line)):
                # Check for any text after @@ <something> @@ and fix it
                # as google's lib chokes on it
                chunk = chunk + line
                chunk = chunk + '\n'
            else:
                # Git's patch
                # extract chunk info and prune line seperately
                if(re.search('^@@.*@@', line)):
                    match = re.search('^@@.*@@', line)
                    chunkspec = line[match.start():match.end()]
                    newline = line[match.end():]
                    chunk = chunk + chunkspec + '\n'
                    chunk = chunk + newline + '\n'
          
    return chunks

def html_table_row(lhs, rhs, style1, style2, line1, line2):
    output = '<tr><th>' + line1 + '</th><td class="'+ style1 + '" id="old-' + line1 + '"><pre>' + lhs + '</pre></td><th>' + line2 + '</th><td class="' + style2 + '" id="new-' + line2 + '"><pre>' + rhs + '</pre></td></tr>'
    return output
    

def convert_to_html(chunk):
    differ = diff_match_patch()
    patches = differ.patch_fromText(chunk)
    content = ''
    for patch in patches:
        line1 = patch.start1 - 1
        line2 = patch.start2 - 1
        for line in patch.diffs:
            line1 = line1 + 1
            line2 = line2 + 1
            action = line[0]
            text = line[1]
            if(text == '\n' or text == ''):
                text = ' ' # don't allow empty lines as they mess things up
            result = ''
            
            line1s = str(line1)
            line2s = str(line2)
            
            if(action == 0):
                result = html_table_row(text, text, 'whiteback', 'whiteback', line1s, line2s)
            if(action == 1):
                result = html_table_row('', text, 'grayback', 'greenback', line1s, line2s)
            if(action == -1):
                result = html_table_row(text, '', 'redback', 'grayback', line1s, line2s)
            content = content + result + '\n'
    return content
    
def process_header_string(header):
    """
    Process the header string of the chunk
    ie --- Something.cc <timestamp> and so on
    and return the title to be used in the page
    """
    # For now, just strip out the first 4 characters
    return header[4:]

def process_chunk(chunk):
    chunkHTML = convert_to_html(chunk[2])
    newFile = process_header_string(chunk[0])
    oldFile = process_header_string(chunk[1])
    
    # return a tuple in the expected format
    return (newFile, oldFile, chunkHTML)
        
def PatchToHtml(parent, patchText):
    assert(isinstance(parent, Patch))
    
    # Try parsing the patch text into chunks
    try:
        chunks = split_into_chunks(patchText)
    except:
        print "Splitting to chunks failed"
        # Fail. Don't process patch
        return False
    
    # process one chunk at a time
    for chunk in chunks:
        # Database objects
        dbChunk = Chunk()
        dbChunk.patch = parent
        
        try:
            pChunk = process_chunk(chunk)
        except:
            print "Processing chunk failed"
            # processing into chunk failed
            return False
                
        dbChunk.chunkText = chunk[2]
        dbChunk.chunkHtml = pChunk[2]
        dbChunk.newFile = pChunk[0]
        dbChunk.originalFile = pChunk[1]
        
        # Save to database
        dbChunk.save()
        
    # Finished successfully
    return True