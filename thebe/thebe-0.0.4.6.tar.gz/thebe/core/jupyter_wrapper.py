from jupyter_client.manager import start_new_kernel
import thebe.core.file as File
import thebe.core.constants as Constant
import thebe.core.output as output 
import thebe.core.logger as Logger
import thebe.core.database as Database
import thebe.core.html as Html
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer, MarkdownLexer
from pygments.formatters import HtmlFormatter
import pypandoc, time, sys, datetime, glob, re, sys, time, os, copy, logging, threading, queue, json

class jupyter_client_wrapper:
    def __init__(self, fileName):
        # Setting up self.loggers
        self.lUpdate = Logger.getLogger('update.log', 'update')
        self.logger = Logger.getLogger('main.log', 'main')
        self.mess_logger = Logger.getLogger('mess.log', 'mess')
        self.status_logger = Logger.getLogger('status.log', 'status')
        self.execute_logger = Logger.getLogger('execute.log', 'execute')


        self.kernel_manager, self.jupyter_client = start_new_kernel()
        # Determine what kind of file working with
        self.fileLocation, is_ipynb = File.setup(fileName)

        # Initialize some variables
#        self.isActive = False
        self.executionThread = None
        self.Cells = []
        self.executions = 0

        # Initialize local and global scope for old
        # execution engine
        self.LocalScope = {}
        self.GlobalScope = {}

    '''
    -------------------------------
    Setter functions
    -------------------------------
    '''
    def setSocket(self, socketio):
        self.socketio = socketio

    '''
    -------------------------------
    Execution pre-preprocessing
    -------------------------------
    '''

    def execute(self, update = 'changed'):
        #self.Cells = Database.getCells(self.fileLocation)
        if self._isActive():
            self.socketio.emit('flash')
        else:
            if update == 'changed':
                self._execute_changed()

            elif update == 'all':
                self._execute_all()

            elif update == 'connected':
                self._execute_connected()

            elif type(update) == list:
                self._execute_cell(update)

            else:
                pass

        time.sleep(.5)
    '''
    -------------------------------
    Execution pre-preprocessing - Helpers
    -------------------------------
    '''
    def _execute_cell(self, index):
#        self.isActive = True
        self._execute(update = index)
#        self.isActive = False

    def _execute_changed(self):
        if self._isModified():
            self.status_logger.info('Execute changed...')
#            self.isActive = True
            self._execute(update = 'changed')
#            self.isActive = False
            self.status_logger.info('Finished...')

    def _execute_all(self):
        self.status_logger.info('Execute all...')
#        self.isActive = True
        self.Cells = []
        self._execute(update = 'all')
#        self.isActive = False
        self.status_logger.info('Finished...')

    def _execute_connected(self):
        if not self.Cells:
            self.status_logger.info('Execute connected...')
#            self.isActive = True
            self._execute(update = 'connected')
#            self.isActive = False
            time.sleep(2)
        else: 
            self.socketio.emit('show all', self._convert())

    def _restart_kernel(self):
        self.status_logger.info('Restarting kernel...')
        kernel_manager.restart_kernel()
        while True:
            try:
                io_msg_content = self.jupyter_client.get_iopub_msg(timeout=3)['content']
                time.sleep(.01)

            except queue.Empty:
                break

    def _isModified(self, x=.3):
        '''
        Return true if the target file has been modified in the past x amount of time
        '''

        lastModified=os.path.getmtime(self.fileLocation)
        timeSinceModified=int(time.time()-lastModified)
        if timeSinceModified<=x:
            return True
        else:
            return False

    '''
    -------------------------------
    Execution - Main - Helpers
    -------------------------------
    '''

    def _execute(self, update = 'changed'):
        '''
        Execute cells based on 'update' value
        '''
        self.status_logger.info('Updating...')
        self._update(self._getFileContent(), update)
        self.status_logger.info('Showing...')
        self.socketio.emit('show all', self._convert())
        '''
        '''
        self.status_logger.info('Executing...')
        self.executionThread = threading.Thread(target = self._executeThread)
        self.executionThread.daemon = True
        self.executionThread.start()

    def _update(self, fileContent, update):
        '''
        Update the 'Cells' variable with new data from
        the Thebe file
        '''

        # 'cells' is for the new cells
        cells = []

        # Ignore code that comes before the first delimiter
        ignoreFirst = self._ignoreFirst(fileContent)
        self.lUpdate.info('---------------')
        self.lUpdate.info('ignoreFirst: %s'%(ignoreFirst,))
        # True cell count, used because sourceCount
        # can be unreliable
        cellCount = 0

        for sourceCount, source in enumerate(fileContent.split(Constant.CellDelimiter)):

            self.lUpdate.info('---------------')
            self.lUpdate.info('Cell count: %s'%(cellCount,))
            # Ignore the first source if a cell delimiter
            # does not preceed it
            if ignoreFirst:
                ignoreFirst = False
                continue

            #Split source by line
            source = source.splitlines(True)
            self.lUpdate.info('Source length: %s'%(len(source),))

            if self._validSource(source):
                # Get copy of cell initially populated
                cell = copy.deepcopy(Constant.Cell)

                cell = self._setMarkdown(source, cell)
                self.lUpdate.info('Changed: %s'%(cell['changed'],))

                # Handle front end buttons
                if update == 'all':
                    cell = self._setChanged(source, cell, force_change = True)
                elif type(update) == list and cellCount in update:
                        cell = self._setChanged(source, cell, force_change = True)
                else:
                    cell = self._setChanged(source, cell)
                self.lUpdate.info('Changed: %s'%(cell['changed'],))

                # Set execution counter if it exists previously
                try:
                    cell['execution_count'] = self.Cells[cellCount]['execution_count'] 
                except IndexError:
                    pass
                cells.append(cell)
                cellCount  += 1

        self.Cells = cells
        self.status_logger.info('Changed cells: %s'%([x['changed'] for x in self.Cells],))

    def _executeThread(self):
        '''
        Run the newly changed cells and return their output.
        '''
        self.status_logger.info('Inside execute thread...')
        self.Cells = self._runNewCells()
        self.executions += 1

        '''
        Update the database with the fresh code.
        And outputs.
        '''
#        Database.update(self.fileLocation, self.Cells, GlobalScope, LocalScope, executions)
        self._updateIpynb()
        self.status_logger.info('Execution thread finished...')
    '''
    -------------------------------
    Actual execution
    -------------------------------
    '''
    def _runNewCells(self):
        '''
        Run each changed cell, returning the output.
        '''

        # Append cells containing updated output to this
        newCells = []

        # Toggle to true when the users code produces an
        # error so code execution can stop
        kill = False

        for cellCount, cell in enumerate(self.Cells):

            # Run changed code if it is not markdown
            # and no prior cell has triggered an error
            if cell['changed']:

                self.socketio.emit('message', 'Running cell #%s...'%(cellCount))
                self.socketio.emit('loading', cellCount)
                cell['changed'] = False
                if cell['cell_type'] != 'markdown' and not kill:
                    self.logger.info('\n------------------------\nRunning cell #%s\nIn directory: %s\nWith code:\n%s\n-------------------------------'%(cellCount, os.getcwd(), cell['source']))

                    # Execute the code from the cell, stream 
                    # outputs using socketio, and return output
                    outputs = self._jExecute(cell['source'])

                    # Prevent subsequent execution of code
                    # if in error was found
                    if self._hasError(outputs):
                        kill = True

                    # Add output data to cell
                    cell['outputs'] = outputs

                    # How does ipython do this?
                    cell['execution_count'] = cell['execution_count'] + 1

            # Append run cell the new cell list
            newCells.append(cell)

        # Stop the front end loading
        self.socketio.emit('stop loading')
        self.status_logger.info('End of runAllCells...')
        return newCells

    def _jExecute(self, code):
        '''
        '''

        self.status_logger.info('Inside jExecute thread...')
        code = ''.join(code)

        # Execute the code
        msg_id = self.jupyter_client.execute(code)

        # Get the execution status
        # When the execution state is "idle" it is complete
        t = True
        try:
            io_msg_content = self.jupyter_client.get_iopub_msg(timeout=1)['content']

        except queue.Empty:
            t = False

        self.status_logger.info('After first message in jExecute...')

        # Initialize the temp variable
        temp = {}

        # Initialize outputs
        outputs = []

        # Continue polling for execution to complete
        # which is indicated by having an execution state of "idle"
        while t:
            # Save the last message content. This will hold the solution.
            # The next one has the idle execution state indicating the execution
            # is complete, but not the stdout output
            temp = io_msg_content
            self.execute_logger.info(temp)
            # Check the message for various possibilities
            if 'data' in temp: # Indicates completed operation
                if 'image/png' in temp['data']:
                    plotData =  temp['data']['image/png']
                    output = self._getPlotOutput(plotData)
                    outputs.append(output)

                    self.socketio.emit('output', output)

            if 'name' in temp and temp['name'] == "stdout": # indicates output
                # Create output for server use
                output = self._getStdOut(temp['text'])
                outputs.append(output)

                # Send HTML output for immediate front end use
                htmlOutput = copy.deepcopy(output)
                htmlOutput['data']['text/plain'] = [Html.convertText(text, ttype = 'bash') for text in htmlOutput['data']['text/plain']]
                self.socketio.emit('output', htmlOutput)

            if 'evalue' in temp: # Indicates error

                # Create output for server use
                output = self._getErr(temp['evalue'])
                outputs.append(output)

                # Send HTML output for immediate front end use
                htmlOutput = copy.deepcopy(output)
                htmlOutput['evalue'] = [Html.convertText(text, ttype = 'bash') for text in htmlOutput['evalue']]
                self.socketio.emit('output', htmlOutput)
                
                # If there is an error than it is pointless 
                # to keep on running code
                break

            # Poll the message
            try:
                io_msg_content = self.jupyter_client.get_iopub_msg(timeout=1)['content']
                time.sleep(.1)

                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    break

            except queue.Empty:
                break

        self.status_logger.info('End of jExecute thread...')
        return outputs

    '''
    -------------------------------
    Execution helper functions
    -------------------------------
    '''
    def _hasError(self, outputs):
        '''
        If an error cell exists in outputs
        return true
        '''
        for output in outputs:
            if 'evalue' in output:
                return True
        return False

    def _fillPlot(cell, plot):
        '''
        If an image exists in the plot variable, create and return a plot cell.
        '''
        if plot:
            output = Constant.getDisplayOutput()
            output['data']['image/png'] = plot
            cell['outputs'].append(output)
        return cell

    def _getPlotOutput(self, plot):
        '''
        '''
        output = Constant.getDisplayOutput()
        output['data']['image/png'] = plot
        return output

    def _getStdOut(self, stdOut):
        output = Constant.getExecuteOutput()
        output['data']['text/plain'] = stdOut.splitlines(True)
        return output

    def _getErr(self, err):
        output = Constant.getErrorOutput()
        output['evalue'] = err.splitlines(True)
        return output
    '''
    -------------------------------
    Preprocessing helper functions
    -------------------------------
    '''

    def _getFileContent(self):
        fileContent = ''
        with open(self.fileLocation, 'r') as file_content:
            fileContent = file_content.read()
        return fileContent

    def _update_all(self):
        # 'cells' is for the new cells
        cells = []


    def _ignoreFirst(self, fileContent):
        # Ignore code that comes before the first delimiter
        if not fileContent.startswith(Constant.CellDelimiter):
            self.logger.info('Ignoring first...')
            return True
        else:
            return False

    def _getSourceList(self):
        '''
        Form the hashes from the cell list into a list
        '''
        return [cell['source'] for cell in self.Cells]

    def _toThebe(self, ipynb):
        '''
        Take in a ipynb dictionary, and returns a string in thebe format.
        (Cell sources to delimited by our Constants.CellDelimiter)
        '''

        output = ''
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'markdown':
                output = ''. join(\
                        (output, \
                        (Constant.CellDelimiter + 'm\n' + \
                        ''.join(cell['source']))\
                        ))
            else:
                output = ''. join(\
                        (output, \
                        (Constant.CellDelimiter + '\n' + \
                        ''.join(cell['source']))\
                        ))
        return output
        

    def _setChanged(self, source, cell, force_change = False):
        '''
        Detect if a cell has been changed
        '''

        if force_change:
            cell['changed'] = True
            cell['last_changed'] = time.strftime("%x %X", time.gmtime())
            cell['outputs'] = []
            
        else:
            try:
                x = self._getSourceList().index(source)
                cell = self.Cells[x]

            except ValueError:
                cell['changed'] = True
                cell['last_changed'] = time.strftime("%x %X", time.gmtime())

        return cell

    def _setMarkdown(self, source, cell):
        '''
        Determine if a cell is marked down
        '''

        # Detect if cell is Markdown
        if source[0] == 'm\n':
            # Set cell as markdown
            cell['cell_type'] = 'markdown'

        # Remove the new line after the delimiter
        source.pop(0)

        #Set sourceCode
        cell['source'] = source

        return cell

    def _validSource(self, source):
        '''
        Return false if source list is all Just new lines
        '''
        for s in source:
            if s != '\n':
                return True
        return False

    def _updateIpynb(self):
        '''
        Write the new changes to the ipynb file.
        '''
        self.status_logger.info('Updating .ipynb...')
        cCells = copy.deepcopy(self.Cells)

        # Remove extra attributes created by thebe.
        self._sanitize(cCells)
        

        # Save cells into a ".ipynb" file
        with open(File.getPrefix(self.fileLocation)+'.ipynb', 'w') as f:
            # Get the jupyter cell list wrapper
            ipynb = Constant.getIpynb()
            # Wrap cells
            ipynb['cells'] = cCells
            # Overwrite old ipynb file
            json.dump(ipynb, f, indent=True)

    def _sanitize(self, Cells):
        '''
        Remove the extra attributes that thebe uses,
        that Jupyter does not
        '''
        for i, cell in enumerate(Cells):
            del Cells[i]['execution_count']
            del Cells[i]['changed']

    '''
    -------------------------------
    HTML conversion
    -------------------------------
    '''

    def _convert(self):
        '''
        Return a deep copy of cellList with code replaced with html-ized code
        '''

        # Deep copy cells so the original is not converted to HTML
        tempCells = copy.deepcopy(self.Cells)


        for cell in tempCells:
            # Preprocessing a code cell
            if cell['cell_type'] == 'code':
                # Highlight the Python syntax
                cell['source'] = \
                        [highlight(source, PythonLexer(), HtmlFormatter()) for source in cell['source']] 
                
                # Highlight standard output and error
                for output in cell['outputs']:
                    # Highlight the standard output
                    if output['output_type'] == 'execute_result':
                        output['data']['text/plain'] = \
                                [highlight(text, BashLexer(), HtmlFormatter()) \
                                for text in output['data']['text/plain']]
                    # Highlight the error
                    if output['output_type'] == 'error':
                        output['traceback'] = \
                                [highlight(text, BashLexer(), HtmlFormatter()) \
                                for text in output['traceback']]

            # Preprocessing a markdown cell
            if cell['cell_type'] == 'markdown':

                # Flatten the list so multi line latex delimiters 
                # are not separated by HTML elements as this would
                # break MathJax.
                cell['source'] = ''.join(cell['source'])

                # Remove any html that could interupt 
                # markdown conversion
                clean = re.compile('<.*>.*</.*>')
                cell['source'] = re.sub(clean, '', cell['source']) 

                # Convert the markdown

                # These arguments are used to let pypandoc
                # know to ignore latex
                pdoc_args = ['--standalone', '--mathjax'] 
                # Convert from markdown to HTML
                cell['source'] = \
                        pypandoc.convert_text(cell['source'], \
                        'html', format = 'md',\
                        extra_args = pdoc_args)

        return tempCells 
    def _isActive(self):
        if  self.executionThread:
            if self.executionThread.is_alive():
                return True
            else:
                return False
        else:
            return False
