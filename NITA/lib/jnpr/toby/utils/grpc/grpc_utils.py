from google.protobuf.json_format import MessageToJson
import json

def grpc_parse_api_response(result,**kwargs):

    """

    This API converts the protobuf type of GRPC API response to a dictionary format
    for ease of accessing the GRPC response keys for offline validation of values.

    :param result  : GRPC API Response object that needs to be parsed 
      *MANDATORY*

    :kwarg concat_key : Name of the key in the grpc streaming result that need to be concatenated 
      *OPTIONAL*        across each chunk in the stream 

    :returns       : A dictionary format of attributes(key-value pairs) returned in GRPC API execution 

    """

    ##create an empty dictionary to hold grpc api exec result
    grpc_result_dict = {}

    if 'concat_key' in kwargs:
       concat_element = kwargs.get('concat_key')
       concat_field = ""

    if hasattr(result, '__iter__'):

       print("\n Parsing a streaming response GRPC API result ... \n")

       # stream object type allows iterating/reading over it once
       # so processs verything inside this for loop once and for all
       # i is stream index
       i = 0
       try:           
          for chunk in result:
             i += 1

             post_res = MessageToJson(chunk,including_default_value_fields=True,preserving_proto_field_name=True)
             post_res_dict = json.loads(post_res)

             if 'concat_key' not in kwargs:

                ### Stream type GRPC API response where each stream's key-value
                ### not co-related to keys in other streams

                strm = "stream" + str(i)
                grpc_result_dict[strm] = dict()

                # to convert list->dict for repeat fields such as repeat1,repeat2 etc.,
                for key,value in post_res_dict.items():
                  if isinstance(value,list):
                    rep = 1
                    rep_key = key + str(rep)
                    for elem in value:
                       rep_key = key + str(rep)
                       grpc_result_dict[strm][rep_key] = elem
                       rep+=1
                  else:
                    grpc_result_dict[strm][key] = value

             else:

                ### Stream type GRPC API response where a particular field in response
                ### is concatenated across all streams

                grpc_result_dict = post_res_dict

                if concat_element in post_res_dict.keys():
                   grpc_res_val = post_res_dict.get(concat_element)
                   concat_field = concat_field + grpc_res_val
                   grpc_result_dict[concat_element] = concat_field
                else:
                   print("\n WARNING: Key ",concat_element," not present in GRPC API response") 
       except Exception:
           # Monitoring done
           print('Monitoring Complete')
           return grpc_result_dict

    else:

       ### Non-stream type GRPC API response ###

       print("\n Parsing a 'NO streaming' response GRPC API result ... \n")

       post_res = MessageToJson(result, including_default_value_fields=True,preserving_proto_field_name=True)
       post_res_dict = json.loads(post_res)

       # to convert list->dict for repeat fields such as repeat1,repeat2 etc.,
       for key,value in post_res_dict.items():
         rep = 1
         rep_key = key + str(rep)
         if isinstance(value,list):
           rep = 1
           rep_key = key + str(rep)
           for elem in value:
             rep_key = key + str(rep)
             grpc_result_dict[rep_key] = elem 
             rep+=1
         else:
            grpc_result_dict[key] = value     

    return grpc_result_dict
