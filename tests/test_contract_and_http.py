import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError
from jsonschema import Draft202012Validator
from tada.fixtures import generate
from tada.__main__ import transform
from tada.core import loads

class OutputTests(unittest.TestCase):
    def test_canonical_schema(self):
        schema=json.loads(Path('schemas/canonical-v1.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator=Draft202012Validator(schema)
        for record in transform(generate()):
            with self.subTest(record=record['id']):validator.validate(record)

    def test_coverage_destinations_resolve(self):
        for record in transform(generate()):
            for source,destination in record['field_coverage'].items():
                if destination=='extensions':self.assertIn(source,record['extensions']);continue
                value=record
                for token in destination[1:].split('/'):
                    key=token.replace('~1','/').replace('~0','~')
                    value=value[int(key)] if isinstance(value,list) else value[key]

    def test_http_round_trip_and_invalid_queries(self):
        with tempfile.TemporaryDirectory() as directory:
            database=str(Path(directory)/'http.sqlite')
            subprocess.run([sys.executable,'-m','tada','ingest','fixtures/synthetic.json','--db',database],check=True,capture_output=True)
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            process=subprocess.Popen([sys.executable,'-m','tada','serve','--db',database,'--port',str(port)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            base=f'http://127.0.0.1:{port}'
            try:
                for _ in range(40):
                    try:
                        with urlopen(base+'/health',timeout=1) as response:self.assertEqual(json.load(response),{'status':'ok'})
                        break
                    except OSError:time.sleep(0.05)
                else:self.fail('Server failed to start')
                with urlopen(base+'/api/stats') as response:self.assertEqual(json.load(response)['total'],21)
                with urlopen(base+'/api/records?provider=ukg-ready&entity=paycheck') as response:
                    records=json.load(response);self.assertEqual(len(records),1);self.assertEqual(records[0]['entity'],'paycheck')
                with urlopen(base+'/') as response:self.assertIn('One model. Three providers.',response.read().decode())
                for path,status in [('/api/records?limit=-1',400),('/missing',404)]:
                    with self.assertRaises(HTTPError) as raised:urlopen(base+path)
                    self.assertEqual(raised.exception.code,status)
                    raised.exception.close()
            finally:
                process.terminate();process.communicate(timeout=5)

if __name__=='__main__':unittest.main()
