. to modify PGE for wvcc, goto its ci from higgs:
  ssh -i ~/.ssh/msas.pem ops@54.167.55.23
  cd /home/ops/pges/mine/matchup_pge

. the input datasets for wvcc are a two-level composition
  . the matchup datasets composed of localize urls of the granules
  . the granules themselves
  . both the above datasets need to be ingested to GRQ

. to prepare for ingest of granules, goto weather
  ssh -Y leipan@weather
  cd $HOME/pge/matchup_pge/util/
  
  where the granule data is
  /raid15/leipan/ingest

. how to get data from weather to mozart
  the rsync command (ran under weather:/raid15/leipan/ingest/VIIRS/1)
  rsync -rave  "ssh -i ~/.ssh/msas.pem" -a * ops@3.84.50.148:/data/input/VIIRS/1/1/.

. to ingest input grandule data for wvcc, goto its mozart from higgs:
  ssh -i ~/.ssh/msas.pem ops@3.84.50.148
  cd /data/input/CrIS
  sh ingest_script.sh
  cd /data/input/VIIRS
  sh ingest_script_viirs.sh

. to generate matchup input dataset on top of the granules, goto weather
  cd $HOME/pge/matchup_pge/util/
  python wvcc_evaluator.py
  to generate a script ingest_matchup.sh along with the input matchup datasets
  which we take to mozart to run

  tar zcvf ~/matchup_cris_viirs.tar.gz ingest_matchup.sh matchup_cris_viirs_20150601T201500_20150601T205500
  scp -i ~/.ssh/msas.pem ~/matchup_cris_viirs.tar.gz ops@3.84.50.148:/data/input/.

  then goto mozart to run: sh ingest_matchup.sh

. to delete documents (datasets) in es database:
  https://www.elastic.co/guide/en/elasticsearch/reference/1.7/docs-delete.html
  curl -XDELETE "http://52.91.25.28:9200/{_index}/{_type}/{_id}"

  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_matchup.cris.viirs/MATCHUP.CRIS.VIIRS/matchup_cris_viirs_20150601T201500_20150601T205500"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_matchup.cris.viirs2/MATCHUP.CRIS.VIIRS2/matchup_cris_viirs_20150601T201500_20150601T205500"

. to query the result:
  (base) leipan@weather2:~/pge/matchup_pge/util [5081] cat search.json
  {"query":{
    bool:{
    must:{"term":{"dataset_type.raw":"MATCHUP-data2"}}
    }
   }
  }

  curl -H "Content-Type: application/json" -X POST -d @search.json "http://52.91.25.28:9200/_search"  (to find out _index, _type, _id for deletion)
  (It works on weather but not mozart. (private vs. public IPs))

. to query and then delete:
  curl -H "Content-Type: application/json" -X POST -d @cris.json "http://52.91.25.28:9200/_search?size=2000" (size=2000 gets 2000 returned items rather than the default 10)
  to find: "_index":"grq_v1.0_sndr.snpp.cris", "_type":"SNDR.SNPP.CRIS", "_id":"SNDR.SNPP.CRIS.20150601T0430.m06.g046.L1B_NSR.std.v02_05.G.180904185403"

  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0324.m06.g035.L1B_NSR.std.v02_05.G.180904185041"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0430.m06.g046.L1B_NSR.std.v02_05.G.180904185403"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0312.m06.g033.L1B_NSR.std.v02_05.G.180904184846"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0018.m06.g004.L1B_NSR.std.v02_05.G.180907215315"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0048.m06.g009.L1B_NSR.std.v02_05.G.180907215401"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0218.m06.g024.L1B_NSR.std.v02_05.G.180904184817"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0242.m06.g028.L1B_NSR.std.v02_05.G.180904184921"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0342.m06.g038.L1B_NSR.std.v02_05.G.180904185239"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0006.m06.g002.L1B_NSR.std.v02_05.G.180907215322"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T0742.m06.g078.L1B_NSR.std.v02_05.G.180904191535"

  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T2048.m06.g209.L1B_NSR.std.v02_05.G.180904200434"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T2018.m06.g204.L1B_NSR.std.v02_05.G.180904200405"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T2030.m06.g206.L1B_NSR.std.v02_05.G.180904200358"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T2036.m06.g207.L1B_NSR.std.v02_05.G.180904200435"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T2024.m06.g205.L1B_NSR.std.v02_05.G.180904200645"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/SNDR.SNPP.CRIS.20150601T2042.m06.g208.L1B_NSR.std.v02_05.G.180904200644"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/"
  curl -XDELETE "http://52.91.25.28:9200/grq_v1.0_sndr.snpp.cris/SNDR.SNPP.CRIS/"



. ---------- how to develop/debug the wvcc PGE/dataset ingest on pleiades ------
. from higgs, login to pleiades, first to sfe1
  alias pleiades='ssh -l lpan -Y sfe1.nas.nasa.gov'
  then
  ssh hfe1

. to test the connections to the wvcc PCM
  server/ip settings are in: /home1/lpan/verdi/ops/hysds/wvcc_celeryconfig.py
  curl http://guest:guest@3.84.50.148:5672
  curl http://:@3.84.50.148
  curl http://52.91.25.28:9200
  curl http://52.91.25.28:8878
  wget --server-response --spider http://34.201.249.63

. to start an interactive celery job
  source wvcc.bashrc
  celery worker --app=hysds --concurrency=1 --loglevel=INFO -Q pleiades_job_worker-small -n 1000 -O fair --without-mingle --without-gossip --heartbeat-interval=60

. to get access to wvcc s3 buckets (wvcc-matchup-code and wvcc-matchup-data)
  ssh higgs
  python /home/leipan/projects/aria_esi/Access-Key-Generation/aws-login-pub.py
  pick 168683381162
  https://github.jpl.nasa.gov/cloud/Access-Key-Generation
  copy the credentials under [saml-pub] to ~/.aws/credentials
  on pleiades under /home1/lpan, and make it [default]

. to develop and integrate the wvcc product dataset
  (see Step 6 of HySDS tutorial)
  on mozart of wvcc
  ~/mozart/etc/datasets.json
  and copy this file to pleiades /home1/lpan/github/job_worker-singularity/datasets.json.wvcc
  after done

