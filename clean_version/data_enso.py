import data_loader

lanina_period1 = data_loader.create_date('2009-01-01', '2009-05-01')['range']
lanina_period2 = data_loader.create_date('2010-06-01', '2012-03-01')['range']
lanina_period3 = data_loader.create_date('2013-05-01', '2013-07-01')['range']
lanina_period4 = data_loader.create_date('2016-10-01', '2016-11-01')['range']
lanina_period5 = data_loader.create_date('2017-07-01', '2018-06-01')['range']

elnino_period1 = data_loader.create_date('2009-07-01', '2009-08-01')['range']
elnino_period2 = data_loader.create_date('2009-10-01', '2009-12-01')['range']
elnino_period3 = data_loader.create_date('2010-01-01', '2010-04-01')['range']
elnino_period4 = data_loader.create_date('2015-05-01', '2016-04-01')['range']
elnino_period5 = data_loader.create_date('2018-08-01', '2018-10-01')['range']