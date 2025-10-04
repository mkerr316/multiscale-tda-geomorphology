# Context
I am trying to make this research project reproducible and scalable on any machine. I would like to make this project as cutting-edge as possible so that I can possibly get published or get funding from this project. I am hoping that it helps my grad school applications (I am applying to Computer Science, Geography, and Math departments at UGA), which are due by the end of the year.

# Project Environment
I have started the following files to improve reproducability:
- Makefile
- Dockerfile
- docker-compose.yml
- environment.yml
- config.yml
- README.md

# Instructions
In general, when we have the choice between two different methods, we want to always choose the most defensible, gold-standard method to make our project enthusiast-grade.

Please always refer to the literature reviews and instructions  in the /docs directory, which is the framework for implementing our code.

Examples of robust, modern, and defensible best practices:
- Use the logging package instead of print()
  - INFO: Default color
  - WARNING: Yellow
  - ERROR: Red
  - CRITICAL: Bold Red
- Use the modern union_all() method instead of unary_union
- Keep all imports at the top of the file
- Use the STAC API provided by Microsoft's Planetary Computer to handle URL signing, since URLS are less stable.
- get_all_items() is deprecated, use item_collection() instead.
