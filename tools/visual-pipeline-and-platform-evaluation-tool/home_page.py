import gradio as gr


class HomePage:
    def __init__(self):
        pass

    # Render the home page
    def render(self):
        with gr.Blocks() as home:
            # Header
            gr.HTML(
                "<div class='spark-header'>"
                "  <div class='spark-header-line'></div>"
                "  <img src='https://www.intel.com/content/dam/logos/intel-header-logo.svg' class='spark-logo'></img>"
                "  <div class='spark-title'>Visual Pipeline and Platform Evaluation Tool</div>"
                "</div>"
            )

            gr.Markdown(
                """
                ## Recommended Pipelines
        
                Below is a list of recommended pipelines you can use to evaluate video analytics performance.
                Click on "Configure and Run" to get started with customizing and benchmarking a pipeline for your
                use case.
                """
            )

            my_button = gr.Button(
                "Go to Pipeline Page",
                link="/smartnvrpipeline"
            )


