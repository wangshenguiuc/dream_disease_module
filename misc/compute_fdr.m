%function compute_fdr(genesetfile)

file_dir = '/data/work/swang141/DreamDiseaseModule/Sheng/analysis/Pascal/Data/PASCAL/output/';
addpath(file_dir)
F = dir([file_dir,'/*.*']);
for threshold = [0.005,0.01,0.05,0.1]
valid_cls = [];
    for ii = 1:length(F)
        if isempty(strfind(F(ii).name,genesetfile))
            continue
        end
        file_name = F(ii).name;
        [cls chipv epv] = textread(file_name,'%d%s%f','headerlines',1);
        fdr = mafdr(epv,'BHFDR',true);        
        valid_cls = [valid_cls;cls(fdr<threshold)];
    end
    fprintf('genesetfile:%s fdr:%f, module:%d, total module:%d\n',genesetfile,threshold,length(valid_cls),length(cls));
end
%end