"""
    Jupyter Interface:: This class contains the core methods to interface with the
    Jupyter notebook.
"""
import os, sys
from IPython.core.display import display, HTML
from .progress import add_progress_listener
from .format import format

def widget():
    display(HTML(format("""
    <script>
        cellDiv = $("div.cell.code_cell:contains('import pynbsim')");
        cellDiv.addClass('widget_cell');
        inputDiv = cellDiv.find('div.input');
        console.log("Initializing pynbsim widget in div:", cellDiv);
        labelShown = 'Hide widget init'; labelHidden = 'Show widget init';
        if(!cellDiv.attr('loaded')) {
            inputDiv.hide();
            inputHidden = true;
            function toggleInput() {
            if(inputHidden) {
                inputDiv.show();
                $("#toggleInput").find('span').html(labelShown);
            } else {
                inputDiv.hide();
                $("#toggleInput").find('span').html(labelHidden);
            }
            inputHidden = !inputHidden;
            }
            $("<div id='toggleInput'></div>")
                .css('position', 'relative')
                .css('top', '-4px')
                .css('left', '-4px')
                .css('cursor', 'pointer')
                .click(toggleInput)
                .insertBefore(cellDiv)
                .append(
                    $("<span>" + labelHidden + "</span>").css('color', '#999').css('font-style', 'italic')
                ).append({powered_by})

            cellDiv.attr('loaded', true);
        }
    </script>
    """)))
    with open(os.path.join(os.path.dirname(__file__), "index.html")) as f:
        display(HTML(f.read()))

def progress_text(token, simulation):
    display(HTML(format("""
        <div id="{{|token|}}"></div>
        <script>
            {{|tag|}}
            $(".inj-{{|token|}}").remove();
            console.log("Adding progress text label?")
            console.log($('#{{|token|}}').length);
            progressTextLabel = $('#{{|token|}}');
            console.log("Progress cell?", progressTextCodeCell);
            console.log("Progress label?", progressTextLabel);
            progressTextCodeCell.prepend({{|powered_by_header|}}.addClass('inj-{{|token|}}'));
            (() => {
                let label = progressTextLabel;
                let icon = $("<i class='fa fa-spinner fa-spin'></i>");
                icon.appendTo(label);
                let text = $("<span style='margin-left: 8px'>Simulation starting...</span>");
                text.appendTo(label);
                let simulation_token = '{{|simulation|}}';
                console.log("IFE", label, simulation_token);
                listenToProgress(simulation_token, progress_event => {
                    if(progress_event.status == 'started') {
                        text.text("Simulation started...");
                    } else if(progress_event.status == 'running') {
                        let progress_message = progress_event.progress;
                        text.text(
                            "Simulated "
                            + progress_message.progression.toString()
                            + " out of "
                            + progress_message.duration.toString()
                            + " milliseconds"
                        )
                    } else if(progress_event.status == 'finished') {
                        text.text("Simulation finished.");
                        icon.removeClass('fa-spinner');
                        icon.removeClass('fa-spin');
                        icon.addClass('fa-check');
                        icon.css('color', 'green');
                    }
                    console.log("progress listen", label, simulation_token, progress_event);
                });
            })()
        </script>
        <style>
            /* Keep the injected blocks alive as long as this output exists */
            .pynbsim-injected-block.inj-{{|token|}} {
                display: block !important;
            }
        </style>""",
        token=token,
        token_var=token.replace("-", "_"),
        tag=tag_code_cell(token, "progressTextCodeCell"),
        simulation=simulation
    )))

def tag_code_cell(unique, var="codeCell"):
    return format("""
            {{|var|}} = $("div.cell.code_cell:contains('{{|unique|}}')");
            console.log("var", {{|var|}});
        """,
        unique=unique,
        var=var
    )

def init_page():
    display(HTML("""<script>
        // Load FontAwesome kit.
        $.getScript("https://kit.fontawesome.com/aceb3af2d4.js", function(){});
        // Apply global styles.
        $(`<style>
            .powered-by-header {
                width: 100%;
                margin-bottom: 4px;
            }

            .powered-by {
                float: right;
                border: #F79862 1.2px solid;
                border-radius: 10px;
                padding: 4px;
                color: wheat;
                font-style: italic;
                background-color: #F79862;
            }

            .powered-by a {
                color: white;
                font-style: normal;
            }
        </style>`).appendTo( "head" );
        // Create listener interface
        var progressListeners = {};
        function reportProgress(token, progress) {
        console.log('received progress for:', token, progress);
            if(!(token in progressListeners)) {
                console.log('No listeners for', token);
                return;
            }
            for(let listener of progressListeners[token]) {
                listener(progress);
            }
        }
        function listenToProgress(token, callback) {
            if(!(token in progressListeners)) {
                progressListeners[token] = []
            }
            progressListeners[token].push(callback);
            console.log('received listener for:', token, callback);
        }
    """))
