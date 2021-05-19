. to delete docker image
  docker rmi --force <IMAGE ID>

. to build docker image, under current dir, which is made the build context
  docker build --rm -t matchup_pge -f docker/Dockerfile .

. to run in interactive bash mode
  docker run -it matchup_pge /bin/bash

  docker run --user 1000:ops -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw -it matchup_pge /bin/bash

. to run match up
  docker run --user 1000:ops -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw -it matchup_pge /home/ops/matchup_pge/run_matchup.sh


