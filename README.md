# Slopmachine

A small python programm to create as much slop websites as you want. 
The Default LLM provider is LM-Studio but can be changed.

### What it does
You type in an idea for a website and how many versions you want of it.

The LLM writes a more detailed prompt which is fed back to the LLM to create a HTML file.

Each "project" is named by the LLM. In each folder you'll find the generated HTML files, a folder for files that don't work as intented, the detailed prompt that was written by the llm and a small documentation with informations about the generation process (used model, time taken to generate, original prompt by used, etc...)

By default the temperature is increased by 3 for each version. The filename contains the temperature used to generate that version.

# See examples
To see examples that were generated using a version of this programm visit [ai.compjej.com](ai.compjej.com)
