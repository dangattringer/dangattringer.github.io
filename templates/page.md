<%*
// --- File Renaming Logic ---
const desiredName = await tp.system.prompt("Enter desired filename (leave blank to cancel):");
let finalName = '';
let renameSuccess = false;
let currentFilePath = tp.file.path(true); // Get the full path *before* potential rename
let cleanFolderName = '';

if (desiredName && desiredName.trim() !== "") {
  let cleanName = desiredName.trim().replace(/[\\/:?*"<>|]/g, '_'); // Basic sanitization
  //cleanName = cleanName.replace(/^\d+-\s*/, '');
	  console.log(cleanName);
      
  if (cleanName === "") {
    new Notice("Invalid filename provided after sanitization.", 3000);
    finalName = tp.file.title; // Use original title
    renameSuccess = false;
  } else {
    try {
      const folderPath = tp.file.folder(true); // Get current folder's full path
	  const folderName = folderPath.split("/").pop(); // Get the last part
      cleanFolderName = folderName.replace(/^\d+-/, ""); // Remove leading number and dash
      console.log(folderName, cleanFolderName)
	  const targetPath = folderPath ? `${folderPath}/${cleanName}.md` : `${cleanName}.md`;
      const existingFile = app.vault.getAbstractFileByPath(targetPath);

      if (existingFile && existingFile.path !== currentFilePath) {
        new Notice(`Error: A file named "${cleanName}.md" already exists in this folder. Rename cancelled.`, 5000);
        finalName = tp.file.title;
        renameSuccess = false;
      } else {
        await tp.file.rename(cleanName);
        new Notice(`File renamed to: ${cleanName}.md`);
        finalName = cleanName;
        currentFilePath = tp.file.path(true); // Update path after successful rename
        renameSuccess = true;
      }
    } catch (error) {
      new Notice(`Error renaming file: ${error}`, 5000);
      console.error("Templater rename error:", error);
      finalName = tp.file.title;
      renameSuccess = false;
      // currentFilePath remains the initial path if rename failed
    }
  }
} else {
  new Notice("File rename cancelled or no name provided.", 2000);
  finalName = tp.file.title;
  renameSuccess = false;
  // currentFilePath remains the initial path
}

// --- Calculate Page Number ---
let pageNumber = 1; // Default page number
const currentFolder = currentFilePath.includes('/') ? currentFilePath.substring(0, currentFilePath.lastIndexOf('/')) : '/'; // Get folder path, handle root

try {
    // Get the TAbstractFile object for the current folder
    const folderObject = app.vault.getAbstractFileByPath(currentFolder === '/' ? '' : currentFolder); // Use '' for root

    // Check if it's a folder by looking for the 'children' property
    if (folderObject && folderObject.children !== undefined) {
        // It's a folder, get its children
        const children = folderObject.children;
        // Filter children to count only files (those *without* a 'children' property)
        const filesInFolder = children.filter(item => item.children === undefined && item.name.toLowerCase() !== 'index.md');
        pageNumber = filesInFolder.length;
    } else if (currentFolder === '/') {
         // Handle root folder specifically if getAbstractFileByPath('') didn't work as expected or we need root files
        const allFiles = app.vault.getFiles(); // This returns only TFile objects
        // Filter files that are directly in the root (path doesn't contain '/')
        const filesInRoot = allFiles.filter(file => !file.path.includes('/') && file.name.toLowerCase() !== 'index.md');
        // Ensure the current file is counted if it's in root and rename failed/was skipped
        // Note: If rename was successful, the file count via getFiles() should be accurate
        pageNumber = filesInRoot.length;
        // Safety check: If the current file path *is* in root, ensure count is at least 1
         if (!currentFilePath.includes('/')&& finalName.toLowerCase() !== 'index.md' && pageNumber === 0) {
            pageNumber = 1;
         }
    } else {
         new Notice(`Warning: Could not accurately determine folder object for path: '${currentFolder}'`, 3000);
    }
} catch (error) {
    new Notice(`Error calculating page number: ${error}`, 5000);
    console.error("Templater page number error:", error);
    // Keep default pageNumber = 1 on error
}

// --- Make variables available for frontmatter ---
_%>---
title: <% finalName %>
author: "Daniel Gattringer"
description: ""
date: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: ["<% cleanFolderName %>"]
page: <% pageNumber %>
---

# <% finalName %>
