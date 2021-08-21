TIMELIMIT_S = 600
HARD_TIMELIMIT_S = 3700
TIMELIMIT = $(shell expr $(TIMELIMIT_S) \* 1000 )
VMEM_LIMIT = 15000000
PYTHON = python3

# Directories
SOL_DIR = solutions
RES_DIR = results
OUT_DIR = output
DZN_DIR = dzn
LOG_DIR = log

# MiniZinc Functions
GECODE_MZN = minizinc --statistics --output-objective --output-time --time-limit $(TIMELIMIT) --solver gecode -o output/$(1)-gecode.out
YUCK_MZN = minizinc --statistics --output-objective --output-time --time-limit $(TIMELIMIT) --solver yuck -o output/$(1)-ycuk.out fzn/$(1).fzn
OSCAR_MZN = minizinc --statistics --output-objective --output-time --time-limit $(TIMELIMIT) -a --solver oscar -o output/$(1)-oscar.out fzn/$(1).fzn
CHUFFED_MZN = minizinc --statistics --output-objective --output-time --time-limit $(TIMELIMIT) -a --solver chuffed -o output/$(1)-chuffed.out fzn/$(1).fzn
ORTOOLS_MZN = minizinc --statistics --output-objective --output-time --time-limit $(TIMELIMIT) -a --solver ortools -o output/$(1)-ortools.out fzn/$(1).fzn

# FlatZinc Functions
GECODE_FZN = fzn-gecode -s -n 0 -a 1 fzn/$(1).fzn > output/$(1)-gecode.out
CHUFFED_FZN = fzn-chuffed -a -v fzn/$(1).fzn > output/$(1)-chuffed.out
ORTOOLS_FZN = fzn-or-tools -statistics=true -all_solutions=true fzn/$(1).fzn > output/$(1)-ortools.out
OSCAR_FZN = fzn-oscar-cbls -a -s -t $(TIMELIMIT_S) fzn/$(1).fzn > output/$(1)-oscar.out
YUCK_FZN = yuck -J-Xmx12g --runtime-limit $(TIMELIMIT_S) -v fzn/$(1).fzn > output/$(1)-yuck.out

TESTCMD = /bin/bash -c "ulimit -S -v $(VMEM_LIMIT); /usr/bin/time -a -o log/$(1).log  /usr/bin/timeout -s 0 $(HARD_TIMELIMIT_S) $(2)"
ITC2FZN = $(PYTHON) src/itc2fzn.py -i data/$(1).xml -o fzn/$(1).fzn --include_names true
FZNPOSTPROCESS = $(PYTHON) src/fzn_postprocess.py -n $(1) -i data/$(1).xml -o output/$(1)-$(2).out -r solutions/$(1)-$(2).xml 
GETRESULT = curl -u brped13@student.sdu.dk -H "Content-Type:text/xml;charset=UTF-8" -d @solutions/$(1)-$(2).xml https://www.itc2019.org/itc2019-validator > results/$(1)-$(2).json


all: data solve

# FlatZinc specific

test1: fzn-aghggisspr-preprocess 
	#./test-util/run_test.sh oscar bet-sum18 0
	$(call OSCAR_FZN,agh-ggis-spr17)

test1-post:
	$(call FZNPOSTPROCESS,bet-sum18,oscar)

fzn-wbgfal: fzn-wbgfal-preprocess
	./test-util/seq_test.sh wbg-fal10 >> log/wbg-fal10.log

fzn-lumssum: fzn-lumssum-preprocess
	./test-util/seq_test.sh lums-sum17 >> log/lums-sum17.log

fzn-betsum: fzn-betsum-preprocess
	./test-util/seq_test.sh bet-sum18 >> log/bet-sum18.log

fzn-pucsfal: fzn-pucsfal-preprocess
	./test-util/seq_test.sh pu-cs-fal07 >> log/pu-cs-fal07.log
	
fzn-pullrspr07: fzn-pullrspr07-preprocess
	./test-util/seq_test.sh pu-llr-spr07 >> log/pu-llr-spr07.log

fzn-puc8spr: fzn-puc8spr-preprocess
	./test-util/seq_test.sh pu-c8-spr07 >> log/pu-c8-spr07.log

fzn-aghfisspr: fzn-aghfisspr-preprocess
	./test-util/seq_test.sh agh-fis-spr17 >> log/agh-fis-spr17.log

fzn-aghggisspr: fzn-aghggisspr-preprocess
	./test-util/seq_test.sh agh-ggis-spr17 >> log/agh-ggis-spr17.log

fzn-betfal: fzn-betfal-preprocess
	./test-util/seq_test.sh bet-fal17 >> log/bet-fal17.log

fzn-ikufal: fzn-ikufal-preprocess
	./test-util/seq_test.sh iku-fal17 >> log/iku-fal17.log

fzn-maryspr: fzn-maryspr-preprocess
	./test-util/seq_test.sh mary-spr17 >> log/mary-spr17.log

fzn-munifispr: fzn-munifispr-preprocess
	./test-util/seq_test.sh muni-fi-spr16 >> log/muni-fi-spr16.log

fzn-munifspsspr: fzn-munifspsspr-preprocess
	./test-util/seq_test.sh muni-fsps-spr17 >> log/muni-fsps-spr17.log

fzn-munipdfspr: fzn-munipdfspr-preprocess
	./test-util/seq_test.sh muni-pdf-spr16c >> log/muni-pdf-spr16c.log

fzn-pullrspr17: fzn-pullrspr17-preprocess
	./test-util/seq_test.sh pu-llr-spr17 >> log/pu-llr-spr17.log

fzn-tgfal: fzn-tgfal-preprocess
	./test-util/seq_test.sh tg-fal17 >> log/tg-fal17.log

fzn-preprocess:
	./test-util/preprocess_test.sh 

fzn-wbgfal-preprocess:
	$(call ITC2FZN,wbg-fal10)

fzn-lumssum-preprocess:
	$(call ITC2FZN,lums-sum17)

fzn-betsum-preprocess:
	$(call ITC2FZN,bet-sum18)

fzn-pucsfal-preprocess:
	$(call ITC2FZN,pu-cs-fal07)

fzn-pullrspr07-preprocess:
	$(call ITC2FZN,pu-llr-spr07)

fzn-puc8spr-preprocess:
	$(call ITC2FZN,pu-c8-spr07)

fzn-aghfisspr-preprocess:
	$(call ITC2FZN,agh-fis-spr17)

fzn-aghggisspr-preprocess:
	$(call ITC2FZN,agh-ggis-spr17)

fzn-betfal-preprocess:
	$(call ITC2FZN,bet-fal17)

fzn-ikufal-preprocess:
	$(call ITC2FZN,iku-fal17)

fzn-maryspr-preprocess:
	$(call ITC2FZN,mary-spr17)

fzn-munifispr-preprocess:
	$(call ITC2FZN,muni-fi-spr16)

fzn-munifspsspr-preprocess:
	$(call ITC2FZN,muni-fsps-spr17)

fzn-munipdfspr-preprocess:
	$(call ITC2FZN,muni-pdf-spr16c)

fzn-pullrspr17-preprocess:
	$(call ITC2FZN,pu-llr-spr17)

fzn-tgfal-preprocess:
	$(call ITC2FZN,tg-fal17)





mzn-wbgfal:
	$(PYTHON) src/preprocess.py -f data/bet-sum18.xml -o dzn/wbg-fal10.dzn
	minizinc -d dzn/wbg-fal10.dzn --solver yuck $(mzn_pars) -o output/wbg-fal10-yuck.out mzn/base.mzn

mzn-aghfisspr:
	$(PYTHON) src/preprocess.py -f data/agh-fis-spr17.xml -o dzn/agh-fis-spr17.dzn

mzn-betsum:
	$(PYTHON) src/preprocess.py -f data/bet-sum18.xml -o dzn/bet-sum18.dzn
	minizinc --solver gecode -d dzn/bet-sum18.dzn mzn/base.mzn

mzn-betfal:
	$(PYTHON) src/preprocess.py -f data/bet-fal17.xml -o dzn/bet-fal17.dzn
	minizinc -d dzn/bet-fal17.dzn --solver gecode $(mzn_pars) -o output/bet-fal17-gecode.out mzn/base.mzn 

mzn-lumssum:
	$(PYTHON) src/preprocess.py -f data/lums-sum17.xml -o dzn/lums-sum17.dzn
	minizinc $(GECODE_PARS) -d dzn/lums-sum17.dzn mzn/base.mzn

mzn-tgfal:
	$(PYTHON) src/preprocess.py -f data/tg-fal17.xml -o dzn/tg-fal17.dzn
	minizinc -d dzn/tg-fal17.dzn --solver yuck $(mzn_pars) -o output/tg-fal17-yuck.out mzn/base.mzn 

mzn-pucsfal:
	$(PYTHON) src/preprocess.py -f data/pu-cs-fal07.xml -o dzn/pu-cs-fal07.dzn
	#minizinc -d dzn/pu-cs-fal07.dzn --solver oscar $(mzn_pars) -o output/pu-cs-fal07-oscar.out mzn/base.mzn
	minizinc $(CHUFFED_PARS) -d dzn/pu-cs-fal07.dzn mzn/base.mzn
	#minizinc $(GECODE_PARS) -d dzn/pu-cs-fal07.dzn mzn/base.mzn

mzn-munifispr:
	$(PYTHON) src/preprocess.py -f data/muni-fi-spr16.xml -o dzn/muni-fi-spr16.dzn
	minizinc $(GECODE_PARS) -d dzn/muni-fi-spr16.dzn -o output/muni-fi-spr16-yuck.out mzn/base.mzn

mzn-munifspsspr:
	$(PYTHON) src/preprocess.py -f data/muni-fsps-spr17.xml -o dzn/muni-fsps-spr17.dzn
	minizinc -d dzn/muni-fsps-spr17.dzn --solver gecode $(mzn_pars) -a -o output/muni-fsps-spr17-gecode.out mzn/base.mzn

dirs:
	mkdir -p $(SOL_DIR)
	mkdir -p $(OUT_DIR)
	mkdir -p $(DZN_DIR)
	mkdir -p $(LOG_DIR)

flat2:
	minizinc --solver gecode -c -d $(DZN_DIR)/wbg-fal10.dzn --fzn fzn/wbg-fal10-gecode2.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/lums-sum17.dzn --fzn fzn/lums-sum17-gecode2.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/bet-sum18.dzn --fzn fzn/bet-sum18-gecode2.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/pu-cs-fal07.dzn --fzn fzn/pu-cs-fal07-gecode2.fzn mzn/base.mzn 


flatten: 
	#minizinc --solver oscar -c -d $(DZN_DIR)/wbg-fal10.dzn --output-fzn-to-file fzn/wbg-fal10-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/lums-sum17.dzn --fzn fzn/lums-sum17-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/bet-sum18.dzn --fzn fzn/bet-sum18-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/pu-cs-fal07.dzn --fzn fzn/pu-cs-fal07-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/pu-c8-spr07.dzn --fzn fzn/pu-c8-spr07-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/mary-spr17.dzn --fzn fzn/mary-spr17-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/muni-fi-spr16.dzn --fzn fzn/muni-fi-spr16-oscar.fzn mzn/base.mzn 
	#minizinc --solver oscar -c -d $(DZN_DIR)/tg-fal17.dzn --fzn fzn/tg-fal17-oscar.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/wbg-fal10.dzn --fzn fzn/wbg-fal10-gecode.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/lums-sum17.dzn --fzn fzn/lums-sum17-gecode.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/bet-sum18.dzn --fzn fzn/bet-sum18-gecode.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/pu-cs-fal07.dzn --fzn fzn/pu-cs-fal07-gecode.fzn mzn/base.mzn 
	#minizinc --solver gecode -c -d $(DZN_DIR)/pu-c8-spr07.dzn --fzn fzn/pu-c8-spr07-gecode.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/mary-spr17.dzn --fzn fzn/mary-spr17-gecode.fzn mzn/base.mzn 
	minizinc --solver gecode -c -d $(DZN_DIR)/muni-fi-spr16.dzn --fzn fzn/muni-fi-spr16-gecode.fzn mzn/base.mzn 
	#minizinc --solver gecode -c -d $(DZN_DIR)/tg-fal17.dzn --fzn fzn/tg-fal17-gecode.fzn mzn/base.mzn 
	minizinc --solver yuck -c -d $(DZN_DIR)/wbg-fal10.dzn --fzn fzn/wbg-fal10-yuck.fzn mzn/base.mzn 
	minizinc --solver yuck -c -d $(DZN_DIR)/lums-sum17.dzn --fzn fzn/lums-sum17-yuck.fzn mzn/base.mzn 
	minizinc --solver yuck -c -d $(DZN_DIR)/bet-sum18.dzn --fzn fzn/bet-sum18-yuck.fzn mzn/base.mzn 
	minizinc --solver yuck -c -d $(DZN_DIR)/pu-cs-fal07.dzn --fzn fzn/pu-cs-fal07-yuck.fzn mzn/base.mzn 
	#minizinc --solver yuck -c -d $(DZN_DIR)/pu-c8-spr07.dzn --fzn fzn/pu-c8-spr07-yuck.fzn mzn/base.mzn 
	minizinc --solver yuck -c -d $(DZN_DIR)/mary-spr17.dzn --fzn fzn/mary-spr17-yuck.fzn mzn/base.mzn 
	minizinc --solver yuck -c -d $(DZN_DIR)/muni-fi-spr16.dzn --fzn fzn/muni-fi-spr16-yuck.fzn mzn/base.mzn 
	#minizinc --solver yuck -c -d $(DZN_DIR)/tg-fal17.dzn --fzn fzn/tg-fal17-yuck.fzn mzn/base.mzn 



data: dirs 
	$(PYTHON) src/preprocess.py -f data/wbg-fal10.xml -o $(DZN_DIR)/wbg-fal10.dzn
	$(PYTHON) src/preprocess.py -f data/lums-sum17.xml -o $(DZN_DIR)/lums-sum17.dzn
	$(PYTHON) src/preprocess.py -f data/bet-sum18.xml -o $(DZN_DIR)/bet-sum18.dzn
	$(PYTHON) src/preprocess.py -f data/pu-cs-fal07.xml -o $(DZN_DIR)/pu-cs-fal07.dzn
	#$(PYTHON) src/preprocess.py -f data/pu-llr-spr07.xml -o $(DZN_DIR)/pu-llr-spr07.dzn
	$(PYTHON) src/preprocess.py -f data/pu-c8-spr07.xml -o $(DZN_DIR)/pu-c8-spr07.dzn
	#$(PYTHON) src/preprocess.py -f data/agh-fis-spr17.xml -o $(DZN_DIR)/agh-fis-spr17.dzn
	#$(PYTHON) src/preprocess.py -f data/agh-ggis-spr17.xml -o $(DZN_DIR)/agh-ggis-spr17.dzn
	#$(PYTHON) src/preprocess.py -f data/bet-fal17.xml -o $(DZN_DIR)/bet-fal17.dzn
	#$(PYTHON) src/preprocess.py -f data/iku-fal17.xml -o $(DZN_DIR)/iku-fal17.dzn
	$(PYTHON) src/preprocess.py -f data/mary-spr17.xml -o $(DZN_DIR)/mary-spr17.dzn
	$(PYTHON) src/preprocess.py -f data/muni-fi-spr16.xml -o $(DZN_DIR)/muni-fi-spr16.dzn
	#$(PYTHON) src/preprocess.py -f data/muni-fsps-spr17.xml -o $(DZN_DIR)/muni-fsps-spr17.dzn
	#$(PYTHON) src/preprocess.py -f data/muni-pdf-spr16c.xml -o $(DZN_DIR)/muni-pdf-spr16c.dzn
	#$(PYTHON) src/preprocess.py -f data/pu-llr-spr17.xml -o $(DZN_DIR)/pu-llr-spr17.dzn
	$(PYTHON) src/preprocess.py -f data/tg-fal17.xml -o $(DZN_DIR)/tg-fal17.dzn
	
postprocess:
	$(PYTHON) src/postprocess.py -n pu-cs-fal07 -i data/pu-cs-fal07.xml -o output/pu-cs-fal07-yuck.out -r solutions/pu-cs-fal07-yuck.xml
	$(PYTHON) src/postprocess.py -n lums-sum17 -i data/lums-sum17.xml -o output/lums-sum17-yuck.out -r solutions/lums-sum17-yuck.xml
	$(PYTHON) src/postprocess.py -n bet-sum18 -i data/bet-sum18.xml -o output/bet-sum18-yuck.out -r solutions/bet-sum18-yuck.xml

sunnycp:
	#minizinc -c mzn/base.mzn dzn/lums-sum17.dzn
	# minizinc -c mzn/base.mzn dzn/agh-fis-spr17.dzn
	# minizinc -c mzn/base.mzn dzn/bet-sum18.dzn
	# minizinc -c mzn/base.mzn dzn/bet-fal17.dzn
	# minizinc -c mzn/base.mzn dzn/pu-cs-fal07.dzn
	# minizinc -c mzn/base.mzn dzn/mary-spr17.dzn
	#timelimit 600s sunny-cp -P yuck,gecode,ortools,chuffed,choco mzn/base.mzn dzn/lums-sum17.dzn | solns2out mzn/base.ozn
	# sunny-cp -P yuck,gecode,ortools,chuffed,choco mzn/base.mzn dzn/agh-fis-spr17.dzn | solns2out mzn/base.ozn
	
	# minizinc -c mzn/base.mzn dzn/bet-sum18.dzn
	# timeout 600s sunny-cp -P ortools,chuffed,choco mzn/base.mzn dzn/bet-sum18.dzn | solns2out mzn/base.ozn > output/bet-sum18-scp.out
	minizinc -c mzn/base.mzn dzn/bet-sum18.dzn
	timeout 60s sunny-cp -P ortools mzn/base.mzn dzn/bet-sum18.dzn | solns2out mzn/base.ozn

	# sunny-cp -P yuck,gecode,ortools,chuffed,choco mzn/base.mzn dzn/bet-fal17.dzn | solns2out mzn/base.ozn
	# sunny-cp -P yuck,gecode,ortools,chuffed,choco mzn/base.mzn dzn/pu-cs-fal07.dzn | solns2out mzn/base.ozn
	# sunny-cp -P yuck,gecode,ortools,chuffed,choco mzn/base.mzn dzn/mary-spr17.dzn | solns2out mzn/base.ozn
	# sunny-cp -P yuck,gecode,ortools,chuffed,choco mzn/base.mzn dzn/p
