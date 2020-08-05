. to modify PGE for wvcc, goto its ci from higgs:
  ssh -i ~/.ssh/msas.pem ops@54.167.55.23
  cd /home/ops/pges/mine/matchup_pge

. to prepare for ingest, goto weather
  ssh -Y leipan@weather
  cd $HOME/pge/matchup_pge/util/
  
  where the data is
  /raid15/leipan/ingest

. to ingest for wvcc, goto its mozart from higgs:
  ssh -i ~/.ssh/msas.pem ops@3.84.50.148
  cd /data/input

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

