def your_model():

    niceNames = {
    'int': 'intervention',
    'qua': 'environmental flow',
    'lei': 'leisure use of river',
    'pri': 'water price',
    'sat': 'satisfaction with water authority',
    'eng': 'engagement of stakeholders',
    }

    responsesList = ['int_eng','int_sat','int_pri','int_lei','int_qua']

    collectedResponses = [
      ('neg',       'neg',       'neg',       'neg',       'neg'), 
      ('neg',       'neg',       'neg',       'neg',       'pos'), 
      ('neg',       'neg',       'neg',       'pos',       'pos'), 
      ('neg',       'neg',       'pos',       'neg',       'neg'), 
      ('neg',       'neg',       'pos',       'neg',       'pos'), 
      ('neg',       'neg',       'pos',       'pos',       'pos'), 
      ('neg',       'pos',       'neg',       'neg',       'neg'), 
      ('neg',       'pos',       'neg',       'neg',       'pos'), 
      ('neg',       'pos',       'neg',       'pos',       'pos'), 
      ('pos',       'neg',       'neg',       'neg',       'pos'), 
      ('pos',       'neg',       'neg',       'pos',       'pos'), 
      ('pos',       'pos',       'neg',       'neg',       'neg'), 
      ('pos',       'pos',       'neg',       'neg',       'pos'), 
      ('pos',       'pos',       'neg',       'pos',       'pos'), 
      ('pos',       'pos',       'pos',       'neg',       'pos'), 
      ('pos',       'pos',       'pos',       'pos',       'pos')
      ]

    return responsesList, niceNames, collectedResponses
