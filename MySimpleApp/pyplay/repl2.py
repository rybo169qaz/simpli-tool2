# command_repl.py
from vlc import LogLevel
import sys
import resp_state_qual
import time

from presenter import *
from loguru import logger


lev_debug = logger.level("DEBUG")
print(f'LOG: DEBUG {lev_debug}')

lev_info = logger.level("INFO")
print(f'LOG: INFO {lev_info}')

lev_error = logger.level("ERROR")
print(f'LOG: ERROR {lev_error}')

#logger.add(sys.stdout, format="LOGURU {time} | {level} | {message}")

def show_args(description, the_list):
    print(f'{description}')
    print(f'Num args=={len(the_list)}')
    list_as_string = ' / '.join(the_list)
    print(f'ARGS: /   {list_as_string}  /')

class CommandHandler:
    def __init__(self, presenterobj):
        self.presenterobj = presenterobj
        self.resources = {
            'media': self.handle_presenter,
            'file': self.handle_file,
            'system': self.handle_system,
            # Add more resources here
        }

    def __show_handle__(self, res, vrb, arg_list):
        print(f'Processing: {res} {vrb} >>{arg_list}<<')

    def handle_system(self, res_keyword, verb, args):
        resname = 'System'
        this_func = 'Handling ' + resname + '(' + res_keyword + ')'
        logger.debug(f'{this_func}: verb={verb} >>{str(args)}<<.')
        if verb == 'sleep':
            if len(args) != 1:
                logger.error(f'{this_func}: {verb} {resname} requires 1 arg, but more (or less) given')
                return RespStateQual(resp=RespSuccess.FAILED, qual=RespQualifierCategory.WRONG_NUMBER_OF_PARAMS, qual_val=str(len(args)))
            self.__show_handle__(res_keyword, verb, args)
            time.sleep(int(args[0]))
            return RespStateQual(RespSuccess.GOOD)
        else:
            logger.error(f'{this_func}: Verb ({verb}) is not defined.')
            return RespStateQual(resp=RespSuccess.FAILED, qual=RespQualifierCategory.INVALID_VERB, qual_val=verb)

    def handle_presenter(self, res_keyword, verb, args):
        resname = 'MediaPresenter'
        this_func = 'Handling ' + resname + '(' + res_keyword + ')'
        logger.debug(f'{this_func}: verb={verb} >>{str(args)}<<.')


        if verb == 'select':
            if len(args) != 1:
                logger.error(f'{this_func}: {verb} {resname} requires 1 arg, but more (or less) given')
                return RespStateQual(resp=RespSuccess.FAILED, qual=RespQualifierCategory.WRONG_NUMBER_OF_PARAMS, qual_val=str(len(args)))
            #print(f'Processing: {res_keyword} {verb} {args[0]}')
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.select_media(args[0])
            logger.trace(f'{this_func}: finished performing {verb}')
            return resp

        elif verb == 'play':
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.start_play()
            return resp

        elif verb == 'stop':
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.stop_play()
            return resp

        elif verb == 'duration':
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.get_duration()
            return resp

        elif verb == 'pause':
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.pause()
            return resp

        elif verb == 'close':
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.close()
            return resp

        elif verb == 'isplaying':
            self.__show_handle__(res_keyword, verb, args)
            resp = self.presenterobj.is_playing()
            return resp

        else:
            logger.error(f'{this_func}: Verb ({verb}) is not defined.')
            return RespStateQual(resp=RespSuccess.FAILED, qual=RespQualifierCategory.INVALID_VERB, qual_val=verb)

    def handle_file(self, res_keyword, verb, args):
        if verb == 'read':
            return f"Reading file with args: {args}"
        elif verb == 'write':
            return f"Writing to file with args: {args}"
        else:
            return f"Unknown verb '{verb}' for resource 'file'"

    def dispatch(self, resource, verb, args):
        handler = self.resources.get(resource)
        if handler:
            resp_status = handler(resource, verb, args)
            logger.debug(f'Dispatch: Finished calling Resource Handler.')
            return resp_status
        logger.error(f'Dispatch: Resource Handler is not defined.')
        return RespStateQual(resp=RespSuccess.FAILED, qual=RespQualifierCategory.INVALID_RESOURCE)

def process_line(the_handler, line):
    this_func = 'Process Line'
    logger.debug(f'{this_func} : lineToProces >>{line}<<')
    abort_processing = None
    parts = line.split()
    #if not line or line.lower() == 'exit' or line.lower() == 'q':
    if len(parts) == 0:
        return False

    if line.lower() == 'exit' or line.lower() == 'q':
        abort_processing = True
        return abort_processing
    parts = line.split()
    if len(parts) < 2:
        #print("Error: command must be in the form <resource> <verb> [args...]")
        logger.error(f'{this_func} : command must be in the form <resource> <verb> [args...]')
        abort_processing = False
        return abort_processing
    resource, verb, *args = parts
    #show_args('BEFORE DISPATCH', args)
    result = the_handler.dispatch(resource, verb, args)
    post_execution_desc = f'Resource={resource}, verb={verb}, Args >>{args}<<: Response: {str(result)}'
    #print(post_execution_desc)
    logger.debug(post_execution_desc)
    abort_processing = False
    return abort_processing

def replloop(passed_arg_string=""):
    logger.debug(f'replloop: PASSED >>{passed_arg_string}<<')
    #command_sequence = []
    #command_sequence.append(passed_arg_string)
    command_sequence = passed_arg_string.split(';')
    presntr = Presenter()

    handler = CommandHandler(presntr)
    syntax_txt = "Enter commands in the form: <resource> <verb> <args...>"
    quit_txt = "Type 'exit' to quit."
    print(f'{syntax_txt}\n{quit_txt}')
    #logger.info(f'LOG {syntax_txt}\n{quit_txt}')

    try:
        while len(command_sequence) > 0:
            nxt_cmd = command_sequence.pop(0)
            nxt_cmd = nxt_cmd.strip()
            if len(nxt_cmd) == 0:
                continue
            logger.debug(f'Processing command >>{nxt_cmd}<<')
            resp = process_line(handler, nxt_cmd)
            if resp:
                #print(f'Ending processing initial input')
                logger.debug(f'Ending processing initial input')
                break

        while True:
            #print(f'>')
            #sys.stdout.flush()
            line = input("> ").strip()
            resp = process_line(handler, line)
            if resp:
                logger.debug(f'Ending processing human input')
                break

    except KeyboardInterrupt:
        print("\nExiting...")
        #break
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Error: {e}")



