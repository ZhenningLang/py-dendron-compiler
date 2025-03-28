from typing import Dict

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Markmap</title>
    <style>
      svg.markmap {{
        width: 100%;
        height: 100vh;
      }}
    </style>
    <script src="https://jsd.cdn.zzko.cn/npm/markmap-autoloader@0.18"></script>
  </head>
  <body>
    <div class="markmap">
      <script type="text/template">
        {content}
      </script>
    </div>
  </body>
</html>

"""


class MarkmapCompiler:

    def compile(self, 
                content: str,
                metadata: Dict, 
                content_without_meta: str) -> str:
        return HTML_TEMPLATE.format(content=content)
