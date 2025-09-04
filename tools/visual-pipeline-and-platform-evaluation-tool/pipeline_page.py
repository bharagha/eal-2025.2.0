import gradio as gr
from typing import Dict, Tuple
from gstpipeline import PipelineLoader, GstPipeline

class PipelinePageTemplate:
    def __init__(self, pipeline_name=None):
        self.pipeline_info: Tuple[GstPipeline, Dict] = PipelineLoader.load(pipeline_name.lower())

        self.input_video_player = gr.Video(
            label="Input Video",
            interactive=True,
            show_download_button=True,
            sources="upload",
            elem_id="input_video_player",
        )

        self.output_video_player = gr.Video(
            label="Output Video (File)",
            interactive=False,
            show_download_button=True,
            elem_id="output_video_player",
            visible=True,
        )

        # Output Live Image (for live preview)
        self.output_live_image = gr.Image(
            label="Output Video (Live Preview)",
            interactive=False,
            show_download_button=False,
            elem_id="output_live_image",
            visible=False,
            type="numpy",
        )

        # Pipeline diagram image
        self.pipeline_image = gr.Image(
            value=str(self.pipeline_info[0].diagram()),
            label="Pipeline Diagram",
            elem_id="pipeline_image",
            interactive=False,
            show_download_button=False,
            show_fullscreen_button=False,
        )

        # Best configuration textbox
        self.best_config_textbox = gr.Textbox(
            label="Best Configuration",
            interactive=False,
            lines=2,
            placeholder="The best configuration will appear here after benchmarking.",
            visible=True,
        )

        # Inferencing channels
        self.inferencing_channels = gr.Slider(
            minimum=0,
            maximum=64,
            value=8,
            step=1,
            label="Number of Recording + Inferencing channels",
            interactive=True,
            elem_id="inferencing_channels",
        )

        # Recording channels
        self.recording_channels = gr.Slider(
            minimum=0,
            maximum=64,
            value=8,
            step=1,
            label="Number of Recording only channels",
            interactive=True,
            elem_id="recording_channels",
        )

        # Tracking type
        self.tracking_type = gr.Dropdown(
            label="Object Tracking Type",
            choices=["short-term-imageless", "zero-term", "zero-term-imageless"],
            value="short-term-imageless",
            elem_id="tracking_type",
        )

        # FPS floor
        self.fps_floor = gr.Number(
            label="Set FPS Floor",
            value=30.0,  # Default value
            minimum=1.0,
            interactive=True,
            elem_id="fps_floor",
        )

        # AI stream rate
        self.ai_stream_rate = gr.Slider(
            label="AI Stream Rate (%)",
            value=20,  # Default value
            minimum=0,
            maximum=100,
            step=1,
            interactive=True,
            elem_id="ai_stream_rate",
        )

        # Inference accordion
        self.inference_accordion = gr.Accordion("Inference Parameters", open=True)

        # Object detection model
        # Mapping of these choices to actual model path in utils.py
        self.object_detection_model = gr.Dropdown(
            label="Object Detection Model",
            choices=[
                "SSDLite MobileNet V2 (INT8)",
                "YOLO v5m 416x416 (INT8)",
                "YOLO v5s 416x416 (INT8)",
                "YOLO v5m 640x640 (INT8)",
                "YOLO v10s 640x640 (FP16)",
                "YOLO v10m 640x640 (FP16)",
                "YOLO v8 License Plate Detector (FP32)",
            ],
            value="YOLO v5s 416x416 (INT8)",
            elem_id="object_detection_model",
        )

        # Object detection device
        self.object_detection_device = gr.Dropdown(
            label="Object Detection Device",
            choices="Disabled",#device_choices,
            value="Disabled",#preferred_device,
            elem_id="object_detection_device",
        )

        # Object detection batch size
        self.object_detection_batch_size = gr.Slider(
            minimum=0,
            maximum=32,
            value=0,
            step=1,
            label="Object Detection Batch Size",
            interactive=True,
            elem_id="object_detection_batch_size",
        )

        # Object detection inference interval
        self.object_detection_inference_interval = gr.Slider(
            minimum=1,
            maximum=6,
            value=3,
            step=1,
            label="Object Detection Inference Interval",
            interactive=True,
            elem_id="object_detection_inference_interval",
        )

        # Object Detection number of inference requests (nireq)
        self.object_detection_nireq = gr.Slider(
            minimum=0,
            maximum=4,
            value=0,
            step=1,
            label="Object Detection Number of Inference Requests (nireq)",
            interactive=True,
            elem_id="object_detection_nireq",
        )

        # Object classification model
        # Mapping of these choices to actual model path in utils.py
        self.object_classification_model = gr.Dropdown(
            label="Object Classification Model",
            choices=[
                "Disabled",
                "EfficientNet B0 (INT8)",
                "MobileNet V2 PyTorch (FP16)",
                "ResNet-50 TF (INT8)",
                "PaddleOCR (FP32)",
                "Vehicle Attributes Recognition Barrier 0039 (FP16)",
            ],
            value="ResNet-50 TF (INT8)",
            elem_id="object_classification_model",
        )

        # Object classification device
        self.object_classification_device = gr.Dropdown(
            label="Object Classification Device",
            choices="Disabled",#device_choices + ["Disabled"],
            value="Disabled",#preferred_device,
            elem_id="object_classification_device",
        )

        # Object classification batch size
        self.object_classification_batch_size = gr.Slider(
            minimum=0,
            maximum=32,
            value=0,
            step=1,
            label="Object Classification Batch Size",
            interactive=True,
            elem_id="object_classification_batch_size",
        )

        # Object classification inference interval
        self.object_classification_inference_interval = gr.Slider(
            minimum=1,
            maximum=6,
            value=3,
            step=1,
            label="Object Classification Inference Interval",
            interactive=True,
            elem_id="object_classification_inference_interval",
        )

        # Object classification number of inference requests (nireq)
        self.object_classification_nireq = gr.Slider(
            minimum=0,
            maximum=4,
            value=0,
            step=1,
            label="Object Classification Number of Inference Requests (nireq)",
            interactive=True,
            elem_id="object_classification_nireq",
        )

        # Object classification reclassify interval
        self.object_classification_reclassify_interval = gr.Slider(
            minimum=0,
            maximum=5,
            value=1,
            step=1,
            label="Object Classification Reclassification Interval",
            interactive=True,
            elem_id="object_classification_reclassify_interval",
        )

        self.pipeline_watermark_enabled = gr.Checkbox(
            label="Overlay inference results on inference channels",
            value=True,
            elem_id="pipeline_watermark_enabled",
        )

        self.pipeline_video_enabled = gr.Checkbox(
            label="Enable video output",
            value=True,
            elem_id="pipeline_video_enabled",
        )

        self.live_preview_enabled = gr.Checkbox(
            label="Enable Live Preview",
            value=False,
            elem_id="live_preview_enabled",
        )

        # Run button
        self.run_button = gr.Button("Run")

        # Benchmark button
        self.benchmark_button = gr.Button("Platform Ceiling Analysis")

        # Stop button
        self.stop_button = gr.Button("Stop", variant="stop", visible=False)

        # Metrics plots
        # plots = [
        #     gr.Plot(
        #         value=create_empty_fig(chart_titles[i], y_labels[i]),
        #         label=chart_titles[i],
        #         min_width=500,
        #         show_label=False,
        #     )
        #     for i in range(len(chart_titles))
        # ]

        # Timer for stream data
        self.timer = gr.Timer(1, active=False)

        self.pipeline_information = gr.Markdown(
            f"### {self.pipeline_info[1]['name']}\n{self.pipeline_info[1]['definition']}"
        )

    def on_run(self):
        yield [
            gr.update(visible=False),
            gr.update(value="video_output_path", visible=True),
            "best_result_message",
        ]

    def render(self):
        with gr.Blocks() as pipeline:
            # Handle run button clicks
            self.run_button.click(
                # Update the state of the buttons
                lambda: [
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True),
                ],
                api_name="run_button",
                outputs=[self.run_button, self.benchmark_button, self.stop_button],
                queue=True,
            # )
            # ).then(
            #     # Reset the telemetry plots
            #     lambda: (
            #         globals().update(
            #             stream_dfs=[
            #                 pd.DataFrame(columns=pd.Index(["x", "y"]))
            #                 for _ in range(len(chart_titles))
            #             ]
            #         )
            #         or [
            #             plots[i].value.update(data=[])
            #             for i in range(len(plots))
            #             if hasattr(plots[i], "value") and plots[i].value is not None
            #         ]
            #         or plots
            #     ),
            #     outputs=plots,
            # ).then(
            #     # Start the telemetry timer
            #     lambda: gr.update(active=True),
            #     inputs=None,
            #     outputs=timer,
            ).then(
                # Execute the pipeline and stream live preview (if enabled)
                self.on_run,
                inputs=None,
                outputs=[self.output_live_image, self.output_video_player, self.best_config_textbox],
            # ).then(
            #     # Stop the telemetry timer
            #     lambda: gr.update(active=False),
            #     inputs=None,
            #     outputs=timer,
            # ).then(
            #     # Generate the persistent telemetry data
            #     lambda: [generate_stream_data(i) for i in range(len(chart_titles))],
            #     inputs=None,
            #     outputs=plots,
            ).then(
                # Update the visibility of the buttons
                lambda: [
                    gr.update(visible=True),
                    gr.update(visible=True),
                    gr.update(visible=False),
                ],
                outputs=[self.run_button, self.benchmark_button, self.stop_button],
            )

            # Handle benchmark button clicks
            # benchmark_button.click(
            #     # Update the state of the buttons
            #     lambda: [
            #         gr.update(visible=False),
            #         gr.update(visible=False),
            #         gr.update(visible=True),
            #     ],
            #     outputs=[run_button, benchmark_button, stop_button],
            #     queue=False,
            # ).then(
            #     # Clear output components here
            #     lambda: [
            #         gr.update(value=""),
            #         gr.update(value=None),
            #     ],
            #     None,
            #     [best_config_textbox, output_video_player],
            # ).then(
            #     # Reset the telemetry plots
            #     lambda: (
            #         globals().update(
            #             stream_dfs=[
            #                 pd.DataFrame(columns=pd.Index(["x", "y"]))
            #                 for _ in range(len(chart_titles))
            #             ]
            #         )
            #         or [
            #             plots[i].value.update(data=[])
            #             for i in range(len(plots))
            #             if hasattr(plots[i], "value") and plots[i].value is not None
            #         ]
            #         or plots
            #     ),
            #     outputs=plots,
            # ).then(
            #     # Start the telemetry timer
            #     lambda: gr.update(active=True),
            #     inputs=None,
            #     outputs=timer,
            # ).then(
            #     # Execute the benchmark
            #     on_benchmark,
            #     inputs=components,
            #     outputs=[best_config_textbox],
            # ).then(
            #     # Stop the telemetry timer
            #     lambda: gr.update(active=False),
            #     inputs=None,
            #     outputs=timer,
            # ).then(
            #     # Generate the persistent telemetry data
            #     lambda: [generate_stream_data(i) for i in range(len(chart_titles))],
            #     inputs=None,
            #     outputs=plots,
            # ).then(
            #     # Reset the state of the buttons
            #     lambda: [
            #         gr.update(visible=True),
            #         gr.update(visible=True),
            #         gr.update(visible=False),
            #     ],
            #     outputs=[run_button, benchmark_button, stop_button],
            # )



            # Header
            gr.HTML(
                "<div class='spark-header'>"
                "  <div class='spark-header-line'></div>"
                "  <img src='https://www.intel.com/content/dam/logos/intel-header-logo.svg' class='spark-logo'></img>"
                "  <div class='spark-title'>Visual Pipeline and Platform Evaluation Tool</div>"
                "</div>"
            )
            with gr.Row():
                # Left column
                with gr.Column(scale=2, min_width=300):
                    # Render the pipeline information
                    self.pipeline_information.render()
                    # Render pipeline image
                    self.pipeline_image.render()

                    # Render the run button
                    self.run_button.render()

                    # Render the benchmark button
                    self.benchmark_button.render()

                    # Render the stop button
                    self.stop_button.render()

                    # Render the best configuration textbox
                    self.best_config_textbox.render()

                    # Metrics plots
                    with gr.Row():
                        # Render plots
                        # for i in range(len(plots)):
                        #     plots[i].render()

                        # Render the timer
                        self.timer.render()

                # Right column
                with gr.Column(scale=1, min_width=150):
                    # Video Player Accordion
                    with gr.Accordion("Video Player", open=True):
                        # Input Video Player
                        self.input_video_player.render()

                        # Output Video Player (file)
                        self.output_video_player.render()

                        # Output Live Image (for live preview)
                        self.output_live_image.render()

                    # Pipeline Parameters Accordion
                    with gr.Accordion("Pipeline Parameters", open=True):
                        # Inference Channels
                        self.inferencing_channels.render()

                        # Recording Channels
                        if self.pipeline_info[1]["parameters"]["run"]["recording_channels"]:
                            self.recording_channels.render()

                        # Render tracking_type dropdown
                        self.tracking_type.render()
                        # Whether to overlay result with watermarks
                        self.pipeline_watermark_enabled.render()
                        # Render live_preview_enabled checkbox
                        self.live_preview_enabled.render()

                        # Enable video output checkbox
                        if self.pipeline_info[1]["parameters"]["run"]["video_output_checkbox"]:
                            self.pipeline_video_enabled.render()

                    # Benchmark Parameters Accordion
                    with gr.Accordion(
                            "Platform Ceiling Analysis Parameters", open=False
                    ):
                        # FPS Floor
                        self.fps_floor.render()

                        # AI Stream Rate
                        if self.pipeline_info[1]["parameters"]["benchmark"]["ai_stream_rate"]:
                            self.ai_stream_rate.render()

                    # Inference Parameters Accordion
                    self.inference_accordion.render()
                    with self.inference_accordion:
                        # Object Detection Parameters
                        self.object_detection_model.render()
                        self.object_detection_device.render()
                        self.object_detection_batch_size.render()
                        self.object_detection_inference_interval.render()
                        self.object_detection_nireq.render()

                        # Object Classification Parameters
                        self.object_classification_model.render()
                        self.object_classification_device.render()
                        self.object_classification_batch_size.render()
                        self.object_classification_inference_interval.render()
                        self.object_classification_nireq.render()
                        self.object_classification_reclassify_interval.render()

            # Footer
            gr.HTML(
                "<div class='spark-footer'>"
                "  <div class='spark-footer-info'>"
                "    ©2025 Intel Corporation  |  Terms of Use  |  Cookies  |  Privacy"
                "  </div>"
                "</div>"
            )
        return pipeline