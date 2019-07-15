

# compareRecordsets
#
# Runs thru lists of two record sets and compares the specified fields.  The caller
# may provide no callback, a single callback function or a list of callback functions
# for each event:
#		@onExists
#			The key exists in the @lhsRecordset
#		@onExistsMatch
#			The key exists in the @lhsRecordset and the @fields are equal in the
#			@lhs and @rhs records.
#		@onExistsNoMatch
#			The key exists in the @lhsRecordset and the @fields are not equal in the
# 			@lhs and @rhs records.
#		@onDoesNotExists
#			The key does not exist in @lhsRecordset.
#
# The event callback payload should be either a dictionary or a list of dictionaries
#  with the following keys:
#		params
#			A list or dictionary of additional parameters to pass from the caller to
# 			event when its fired.
#		function
#			A pointer to a function with a @lhs, @rhs.  Additional parameters may be
#			passed via the "params" key described above.
#

def __generateKey(keyFields, record):
	fieldValues = []
	key = "_"

	for key in keyFields:
		if key not in record:
			raise Exception("Key [%s] not found in the record" % (key))

		fieldValues.append(record[key])

	key = key.join(fieldValues)
		

def __generateIndex(records, keys, replace):
	index = {}

	for record in records:
		indexKey = __generateKey(keys, record)
		
	hasKeyAlready = True if indexKey in index else False
	
	if hasKeyAlready and replace:
		index[indexKey] = record
	elif not hasKeyAlready:
		index[indexKey] = record

	return index

def __compareFieldsList(lhs, rhs, fields):
	
	isMatch = True

	for field in fields:

		if field not in lhs:
			raise Exception("Field [%s] not found in @lhs" % (field))

		if field not in rhs:
			raise Exception("Field [%s] not found in @rhs" % (field))

		if lhs[field] != rhs[field]:
			return False

	return True

def __compareFieldsMap(lhs, rhs, fields):
	
	isMatch = True

	for fieldLhs, fieldRhs in fields.iteritems():
		if fieldLhs not in lhs:
			raise Exception("Field [%s] not found in @lhs" % (fieldLhs))

		if fieldRhs not in rhs:
			raise Exception("Field [%s] not found in @rhs" % (fieldRhs))

		if lhs[fieldLhs] != rhs[fieldRhs]:
			return False

	return True

def __compareFields(lhs, rhs, fields):

	funcs = {
		dict: __compareFieldsMap,
		list: __compareFieldsList
	}

	if type(fields) in funcs:
		function = funcs[type(fields)]
		return functions(lhs, rhs, fields)

	raise Exception("@fields object type not supported")


def __fireEventDict(event, localParams=None):
	if not isinstance(event, dict):
		raise Exception("Expected @event to be an instance of dict")

	if "function" not in event:
		raise Exception("Expected a function member in @event")

	function = event["function"]
	localParams = localParams if localParams is not None else []
	hasParams = True if "params" in event else False

	if hasParams:
		params = event["params"]

		#if isinstance(params, list):
		#	function(*localParams, *params)
		#elif isinstance(params, dict):
		#	function(*localParams, **params)
	else:
		function(*localParams)

def __fireEventList(events, localParams=None):
	if not isinstance(events, list):
		raise Exception("Expected @event to be an instance of list")

	for event in events:
		__fireEvent(event, localParams)

def __fireEvent(event, localParams=None):

	funcs = {
		list: __fireEventList,
		dict: __fireEventDict
	}

	if event is None:
		return
	
	if type(event) not in funcs:
		raise Exception("@event is not a support event type")

	function = funcs[type(event)]
	
	if localParams is not None:
		function(event, *localParams)
	else:
		function(event)

def compareRecordsets(lhsRecordset, rhsRecordset, fields, keys, chunkSize, onExists, onExistsMatch, onExistsNoMatch, onDoesNotExist, onChunkFinished, onFinished):

	lhsIndex = generateIndex(lhsRecordset, keys)

	for idx, rhs in rhsRecordset:
		lookupKey = generateKey(keys, record)

		if lookupKey in lhsIndex:
			lhs = lhsIndex[lookupKey]
			
			fireEvent(onExists, [lhs, rhs])

			isMatching = compareFields(lhs, rhs, fields)
			if isMatching:
				fireEvent(onExistsMatch, [lhs, rhs])
			else:
				fireEvent(onExistsNoMatch, [lhs, rhs])
				
		else:
			fireEvent(onDoesNotExist, [lhs, rhs])

		if isinstance(chunkSize, int):
			if idx % chunkSize == 0:
				fireEvent(onChunkFinished)

	fireEvent(onFinished)

	return
