#!/usr/bin/python

import re
import string
from diff_match_patch import diff_match_patch

def split_into_chunks(patch):
    chunks = []
    # Split into lines
    lines = patch.split('\n')
    
    chunk = ''
    originalFile = ''
    newFile = ''
    chunkMode = False
    
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
            continue
            
        if(line[0:3] == "+++"):
            chunkMode = True
            newFile = line
            continue
        
        if ('-+ '.find(line[0]) != -1):
            chunk = chunk + line
            chunk = chunk + '\n'
            continue
        
        if(line[0] == '@'):
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

def html_table_row(lhs, rhs, style1 = "", style2 = ""):
    output = '<tr><td class="'+ style1 + '">' + lhs + '</td><td class="' + style2 + '">' + rhs + '</td></tr>'
    return output
    

def convert_to_html(chunk):
    differ = diff_match_patch()
    patches = differ.patch_fromText(chunk)
    content = ''
    for patch in patches:
        for line in patch.diffs:
            action = line[0]
            text = line[1]
            result = ''
            if(action == 0):
                result = html_table_row(text, text, 'white', 'white')
            if(action == 1):
                result = html_table_row('', text, 'white', 'green')
            if(action == -1):
                result = html_table_row(text, '', 'red', 'white')
            content = content + result + '\n'
    return content
    

def process_chunks(chunks):
    for chunk in chunks:
        print "\n\n <b>Processing a chunk</b> \n\n"
        chunkText = chunk[2]
        print '<table border="1">'
        html = convert_to_html(chunkText)
        print html + '</table>'
        

if(__name__ == "__main__"):
    chunks = split_into_chunks(open('test.patch').read())
    process_chunks(chunks)
