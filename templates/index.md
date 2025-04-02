<%*
const indexFileName = "index.md"; 
const currentFilePath = tp.file.path(true);
const currentFolderPath = tp.file.folder(true); 
const parentFolderPath = currentFolderPath.includes('/') ? currentFolderPath.substring(0, currentFolderPath.lastIndexOf('/')) : '/';
const folderDisplayName = tp.file.folder(false); 
let targetPath = `${currentFolderPath}/${indexFileName}`;

const existingIndex = app.vault.getAbstractFileByPath(targetPath);
if (existingIndex && existingIndex.path !== currentFilePath) {
const errorMsg = `Error: An index file named "${indexFileName}" already exists in this folder. Template aborted.`;
new Notice(errorMsg, 5000);
tR = errorMsg; 
return;
}

let finalName = folderDisplayName;
try {
if (tp.file.name !== indexFileName.replace(".md", "")) {
await tp.file.rename(indexFileName.replace(".md", ""));
new Notice(`File renamed to: ${indexFileName}`);
}
} catch (error) {
const errorMsg = `Error renaming file to ${indexFileName}: ${error}`;
new Notice(errorMsg, 5000);
console.error("Templater index rename error:", error);
tR = errorMsg; 
return;
}

let pageNumber = 1; 
try {
const parentFolderObject = app.vault.getAbstractFileByPath(parentFolderPath === '/' ? '' : parentFolderPath);
if (parentFolderObject && parentFolderObject.children !== undefined) {
const siblings = parentFolderObject.children;
const siblingFolders = siblings.filter(item => item.children !== undefined);
pageNumber = siblingFolders.length;
if (pageNumber === 0) pageNumber = 1;
} else if (parentFolderPath === '/') {
const rootChildren = app.vault.getRoot().children;
const rootSiblingFolders = rootChildren.filter(item => item.children !== undefined);
pageNumber = rootSiblingFolders.length;
if (pageNumber === 0) pageNumber = 1;
} else {
new Notice(`Warning: Could not accurately determine parent folder object for path: '${parentFolderPath}' to count siblings. Defaulting page to 1.`, 3000);
pageNumber = 1; 
}
} catch (error) {
new Notice(`Error calculating page number based on sibling folders: ${error}`, 5000);
console.error("Templater folder page number error:", error);
pageNumber = 1; 
}

_%>---
title: <% folderDisplayName %>
author: "Daniel Gattringer"
description: "Index file for the <% folderDisplayName %> folder."
draft: true
page: <% pageNumber %>
---
# <% folderDisplayName %> 

This is the index file for the **<% folderDisplayName %>** folder. 

Use this page to list and link to the main notes within this section. 

## Key Notes

* [[Link to Note 1]] 
* [[Link to Note 2]] 
* ... 

--- 
