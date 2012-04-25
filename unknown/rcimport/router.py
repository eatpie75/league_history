class RCImport(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label=='rcimport':
			return 'rcimport'
		else:
			return None
	def allow_syncdb(self, db, model):
		if model._meta.app_label=='rcimport':
			return False
		else:
			return True
