python scripts/to_vw_input_format.py --en-file data/chat-P3-data-training-tgt.sgm.line.tok.train.declass.chunked --zh-file data/chat-P3-data-training-src.sgm.line.tok.train.declass.chunked --zh-pos-file data/chat-P3-data-training-src.sgm.line.tok.train.declass.pos  --bow --f-count --s-count --zh-label --pos-tags --verbs --pronouns > data/chat-P3-data-training.input

python scripts/to_vw_input_format.py --en-file data/LDC2013E83-BOLT-P2R2-cmn-SMS-CHT-dev-ref.sgm.tok.lowercase.declass.chunked --zh-file data/LDC2013E83-BOLT-P2R2-cmn-SMS-CHT.sgm.tok.ne.declass.chunked --zh-pos-file data/LDC2013E83-BOLT-P2R2-cmn-SMS-CHT.sgm.tok.ne.declass.pos --bow --f-count --s-count --zh-label --pos-tags --verbs --pronouns > data/LDC2013E83-BOLT-P2R2-cmn-SMS-CHT.input

/fs/clip-bolt/raosudha/SMS_Pronoun/05192014/vowpal_wabbit/vowpalwabbit/vw -b 24 -k -c --ring_size 1024 --passes 10 --search_task sequence --search 5 --search_neighbor_features -2:f,-1:f,1:f,2:f,-2:s,-1:s,1:s,2:s --search_history 3 --holdout_after 3000 --search_rollout oracle --search_alpha 1e-8 -d data/chat-P3-data-training.input -f data/chat-P3-data-training.model

/fs/clip-bolt/raosudha/SMS_Pronoun/05192014/vowpal_wabbit/vowpalwabbit/vw -b 24 -k -c --ring_size 1024 -d data/LDC2013E83-BOLT-P2R2-cmn-SMS-CHT.input -i data/chat-P3-data-training.model -t -p data/LDC2013E83-BOLT-P2R2-cmn-SMS-CHT.predict


