/**
 * Calico Jupyter Notebooks Extensions
 *
 * Copyright (c) The Calico Project
 * http://calicoproject.org/ICalico
 *
 * Released under the BSD Simplified License
 *
 **/

function ip_version() {
    if (IPython.version[0] === "2")
	return 2;
    else if (IPython.version[0] === "3")
	return 3;
    else
	throw "IPython version not supported";
}

function break_into_sections(index) {
    if (ip_version() === 2)
	return 0;
    var cells = IPython.notebook.get_cells();
    var count = 0; // count below index, or -1
    // go in reverse order to keep index accurate
    for (var i = cells.length - 1; i > -1; i--) {
	var cell = cells[i];
	var rendered = cell.rendered;
	// consider it for breaking:
	if (cell.cell_type === "markdown") {
	    var text = cell.get_text();
	    if (text.match(/^#+Table of Contents/)) 
		continue;
	    var lines = text.split(/\n/g);
	    if (lines.length > 1) {
		// possibly break up
		var state = "ok";
		var current = "";
		var cell_texts = [];
		for (var line_no in lines) {
		    var line = lines[line_no];
		    if (state === "ok") {
			if (line.indexOf('```') === 0) {
                            // set state to fence: allows for longer fences
			    state = line.substr(0, line.search("[^`]"));
			    current += line + "\n";
			} else if (line.indexOf('#') === 0) {
			    if (current !== "") {
				cell_texts.push(current.trim());
			    }
			    current = "";
			    cell_texts.push(line);
			} else {
			    current += line + "\n";
			}
		    } else { // in block
			if (line.indexOf(state) === 0) {
			    state = "ok";
			    current += line + "\n";
			    cell_texts.push(current.trim());
			    current = "";
			} else {
			    current += line + "\n";
			}
		    }
		} // for
		// anything left over:
		if (current.trim() !== "") {
		    cell_texts.push(current.trim());
		}
		if (cell_texts.length > 1) {
		    var current_cell = IPython.notebook.get_cell(i);
		    var added = 0;
		    for (var j = 0; j < cell_texts.length; j++) {
			if (cell_texts[j].trim() !== "") {
			    if (added === 0) {
				current_cell.set_text(cell_texts[j]);
				if (rendered) {
				    current_cell.render();
				}					
			    } else {
				if (i === index) {
				    count = -1; // nope, can't do it
				} else if (i < index && count !== -1) {
				    count++;
				}
				var new_cell = IPython.notebook.insert_cell_below("markdown", i + added - 1);
				new_cell.set_text(cell_texts[j]);
                                if (rendered) {
				    new_cell.render();
				}
			    }
			    added++;
			}
		    }
		}
	    }
	}
    }
    return count;
}

function is_heading(cell) {
    if (ip_version() === 2)
	return (cell.cell_type === "heading");
    else 
	return (cell.cell_type === "markdown" && cell.get_text().indexOf("#") === 0)
}

function get_heading_text(cell) {
    if (ip_version() === 2)
	return cell.get_text();
    else if (cell.get_text().indexOf("######") === 0)
	return cell.get_text().substring(6).trim();
    else if (cell.get_text().indexOf("#####") === 0)
	return cell.get_text().substring(5).trim();
    else if (cell.get_text().indexOf("####") === 0)
	return cell.get_text().substring(4).trim();
    else if (cell.get_text().indexOf("###") === 0)
	return cell.get_text().substring(3).trim();
    else if (cell.get_text().indexOf("##") === 0)
	return cell.get_text().substring(2).trim();
    else if (cell.get_text().indexOf("#") === 0)
	return cell.get_text().substring(1).trim();
    else return "";
}

function repeat(pattern, count) {
    if (count < 1) return '';
    var result = '';
    while (count > 1) {
        if (count & 1) result += pattern;
        count >>= 1, pattern += pattern;
    }
    return result + pattern;
}

function set_heading_text(cell, text) {
    var rendered = cell.rendered;
    cell.unrender();
    if (ip_version() === 2)
	cell.set_text(text);
    else {
	var level = get_level(cell);
	cell.set_text( repeat("#", level) + " " + text)
    }
    if (rendered) {
        cell.render();
    }
}

function get_level(cell) {
    if (ip_version() === 2)
	return cell.level;
    else if (cell.get_text().indexOf("######") === 0)
	return 6;
    else if (cell.get_text().indexOf("#####") === 0)
	return 5;
    else if (cell.get_text().indexOf("####") === 0)
	return 4;
    else if (cell.get_text().indexOf("###") === 0)
	return 3;
    else if (cell.get_text().indexOf("##") === 0)
	return 2;
    else if (cell.get_text().indexOf("#") === 0)
	return 1;
    else return 0;
}

function get_last_cell_index_in_section(level, index) {
    var current = index;
    while (IPython.notebook.is_valid_cell_index(current + 1)) {
	var cell = IPython.notebook.get_cell(current + 1);
	if (is_heading(cell) && get_level(cell) <= level) {
	    return current;
	}
	current++;
    }
    return current;
}

function get_index_level_above(level, index) {
    var current = current = index - 1;
    while (IPython.notebook.is_valid_cell_index(current)) {
	var cell = IPython.notebook.get_cell(current);
	if (is_heading(cell) && get_level(cell) <= level) {
	    return current;
	}
	current--;
    }
    return undefined;
}

function get_index_level_below(level, index) {
    var current = current = index + 1;
    while (IPython.notebook.is_valid_cell_index(current)) {
	var cell = IPython.notebook.get_cell(current);
	if (is_heading(cell) && get_level(cell) <= level) {
	    return current;
	}
	current++;
    }
    return undefined;
}

function section_label() {
    // Label headings with numbers, or toggle them off
    // If there is a table of contents, re-do it
    break_into_sections();
    var cells = IPython.notebook.get_cells();
    var levels = [0,0,0,0,0,0];
    var current_level = 1;
    var flag = false;
    var alert_text = "";
    var alert_flag = false;
    var remove_numbering = true;
    
    for (var i = 0; i < cells.length; i++) {
	var cell = cells[i];
	if (is_heading(cell)) {
	    if (cell.get_text().match(/^#+Table of Contents/)) 
		continue;
	    if (cell.get_text().match(/^#+References/)) 
		continue;
	    var level = get_level(cell);
	    
	    if (level >= current_level) { //just keep incrementing
		current_level = level;
		levels[level-1]++;
	    } else {                    //went back a level
		levels[current_level-1] = 0;
		
		if (current_level-level > 1) { //Skipped levels in between
		    for (var j = 1; j < current_level-level; j++) { //back-prop the zeros
			levels[current_level - 1 - j] = 0;
		    }
		}
		
		levels[level -1]++;
		current_level = level;
	    }
	    
	    var error = false;
	    var error_no_begin = 0;
	    var error_no_end = 0;
	    var error_heading_label = "";
	    var heading_label = ""; //Generate the appropriate number for the heading
	    for (var k = 0; k < level; k++) {
		if (levels[k] == 0) {
		    if (!error) {
			error_heading_label = heading_label;
			error = true;
			error_no_begin = k;
		    } else {
			error_no_end = k + 2;
		    }
		}
		heading_label += levels[k];
		if (level-k == 1 && level > 1) {
		    break;
		}
		heading_label += ".";
	    }
	    
	    if (error) {
		if (error_no_end == 0) {
		    error_no_end = error_no_begin + 2;
		}
		if (error_heading_label == "") {
		    if (!flag) {
			var temp1 = "Notebook begins with a Header " + error_no_end + " cell." + "\n";
			alert_text += temp1;
			alert_flag = true;
			flag = true;
		    }
		} else{
		    var temp = "You placed a Header " + error_no_end + " cell under a Header " + error_no_begin + " cell in section " + error_heading_label +"\n";
		    alert_text += temp;
		    alert_flag = true;
		}
	    }
	    
	    var heading_text = get_heading_text(cell);
	    var old_header = heading_text;
	    var re = /(?:\d*\.*)*\s*(.*)/;
	    var match = heading_text.match(re);
	    
	    if (match) {
		heading_text = heading_label + " " + match[1];
	    } else {
		heading_text = heading_label;
	    }
	    
	    if (old_header != heading_text) {
		remove_numbering = false;
		replace_links(old_header, heading_text);
	    }
	    
	    heading_text = heading_text.trim();
	    set_heading_text(cell, heading_text);
	}
    }
    
    if (alert_flag) {
	alert(alert_text);
    }
    
    if (remove_numbering) {
	for (var i = 0; i < cells.length; i++) {
	    var cell = cells[i];
	    if (is_heading(cell)) {
		if (cell.get_text().match(/^#+Table of Contents/)) 
		    continue;
		if (cell.get_text().match(/^#+References/)) 
		    continue;
		var heading_text = get_heading_text(cell);
		old_header = heading_text;
		var re = /(?:\d*\.*)*\s*(.*)/;
		var match = heading_text.match(re);
		if (match) {
		    heading_text = match[1];
		}
		set_heading_text(cell, heading_text);
		replace_links(old_header, heading_text);
	    }
	}
    }
    
    // If there is a Table of Contents, replace it:
    var cells = IPython.notebook.get_cells();
    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        if (cell.cell_type == "markdown") {
	    var cell_text = cell.get_text();
	    var match = cell_text.match(/^#+Table of Contents/);
	    if (match) {
		table_of_contents();
		break;
	    }
	}
    }
}

function replace_links(old_header, new_header) {
    // Replace an old internal link with new link
    new_header = new_header.trim();
    var cells = IPython.notebook.get_cells();
    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        if (cell.cell_type == "markdown") {
	    var cell_text = cell.get_text();
	    // Skip over table of contents:
	    if (cell_text.match(/^#+Table of Contents/)) {
		continue;
	    }
	    var re_string = old_header;
	    re_string = re_string.replace(/\\/g, "\\\\");
	    re_string = re_string.replace(/\//g, "\\/");
	    re_string = re_string.replace(/\^/g, "\\^");
	    re_string = re_string.replace(/\$/g, "\\$");
	    re_string = re_string.replace(/\*/g, "\\*");
	    re_string = re_string.replace(/\+/g, "\\+");
	    re_string = re_string.replace(/\?/g, "\\?");
	    re_string = re_string.replace(/\./g, "\\.");
	    re_string = re_string.replace(/\)/g, "%29");
	    re_string = re_string.replace(/\|/g, "\\|");
	    re_string = re_string.replace(/\[/g, "\\[");
	    re_string = re_string.replace(/\]/g, "\\]");
	    re_string = re_string.replace(/\(/g, "?:\\(|%28");
	    re_string = re_string.replace(/\s/g, "-");
	    re_string = "(\\[.*\\](?::\\s*|\\()#)" + re_string + "(.*\\)|(.*)$)";
	    
	    var re = new RegExp(re_string, "gm");
	    var link_text = new_header.replace(/\s+$/g, ""); //Delete trailing spaces before they become "-"
	    link_text = link_text.replace(/\(/g, "%28"); //Replace left parentheses with their encoding
	    link_text = link_text.replace(/\)/g, "%29"); //Replace right parentheses with their encoding
	    link_text = link_text.replace(/ /g, "-"); //Replace all spaces with dashes to create links
	    
	    var match = cell_text.match(re);
	    if (match) {
                var new_text = cell_text.replace(re, "$1" + link_text + "$2");
                cell.unrender();
                cell.set_text(new_text);
                cell.render();
	    }
        }
    }
}

function find_cell(cell_type, text) {
    // Finds first cell of cell_type that starts with text
    // cell_type and text are interpreted as a regular expression
    var cell = undefined;
    var cells = IPython.notebook.get_cells();
    for (var x = 0; x < cells.length; x++) {
	var temp = cells[x];
	if (temp.cell_type.match(cell_type) != undefined) {
	    var temp_text = temp.get_text();
	    var re = new RegExp("^" + text);
	    if (re.test(temp_text)) {
		cell = cells[x];
		break;
	    }
	}
    }
    return cell;
}

function table_of_contents() {
    break_into_sections();
    // Create and/or replace Table of Contents
    var cells = IPython.notebook.get_cells();
    var toc_cell = find_cell("markdown", "#+Table of Contents");
    // Default to top-level heading
    var toc_text = "#Table of Contents\n";
    if (toc_cell == undefined) {
	//Create a new markdown cell at the top of the Notebook
	toc_cell = IPython.notebook.select(0).insert_cell_below("markdown"); 
    } else {
	// already exists:
	toc_text = toc_cell.get_text().match(/^#+Table of Contents/)[0] + "\n";
    }
    var prev_lev = 0;
    for (var i = 0; i < cells.length; i++) {
	var cell = cells[i];
	if (is_heading(cell)) {
	    if (cell.get_text().match(/^#+Table of Contents/)) 
		continue;
	    if (cell.get_text().match(/^#+References/)) 
		continue;
	    if (get_level(cell) - prev_lev > 1) { //Skipped levels. Enter Dummy levels
		for (var x = 0; x < ((get_level(cell) - prev_lev) - 1); x++) {
		    for (var y = 0; y < (prev_lev + x); y++) {
			toc_text += "\t";
		    }
		    toc_text += "* &nbsp;\n";
		}
	    }
	    var cell_text = get_heading_text(cell);
	    for (var j = 0; j < get_level(cell) -1; j++) { //Loop to add the proper amount of tabs based on header level
		toc_text += "\t";
	    }
	    toc_text += "* [";
	    toc_text += cell_text;
	    toc_text += "](#";
	    var link_text = cell_text.replace(/\s+$/g, ""); //Delete trailing spaces before they become "-"
	    link_text = link_text.replace(/\(/g, "%28"); //Replace left parentheses with their encoding
	    link_text = link_text.replace(/\)/g, "%29"); //Replace right parentheses with their encoding
	    link_text = link_text.replace(/ /g, "-"); //Replace all spaces with dashes to create links
	    toc_text += link_text;
	    toc_text += ")\n";
	    prev_lev = get_level(cell);
	}
    }
    toc_cell.unrender();
    toc_cell.set_text(toc_text);
    toc_cell.render();
}
