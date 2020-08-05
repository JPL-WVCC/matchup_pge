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
  cd /data/input

. to generate matchup input dataset on top of the granules, goto weather
  cd $HOME/pge/matchup_pge/util/
  python wvcc_evaluator.py

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

  curl -H "Content-Type: application/json" -X POST -d @search.json "http://52.91.25.28:9200/_search"  (to find out _index, _type, _id)

