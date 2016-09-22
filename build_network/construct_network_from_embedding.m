addpath 'mashup'
addpath 'read_data'
addpath 'cluster'
addpath 'DCA'
addpath 'build_network'
addpath '../Data/Network/subch2/subchallenge2'

dim_l = [50,500,1000,2000];

% net_file_l ={'1_ppi_anonym_aligned_v2.txt',...
%     '2_ppi_anonym_aligned_v2.txt',...
%     '3_signal_anonym_aligned_directed_v3.txt',...
%     '4_coexpr_anonym_aligned_v2.txt',...
%     '5_cancer_anonym_aligned_v2.txt','6_homology_anonym_aligned_v2.txt'};
% network_file = 'dream_ch2';
% output_path = '../Data/Network/embed_network/subch2/';
% [network, i2g,g2i] = read_multiple_network( net_file_l, false);
% nnet = 6;
% diff = cell(1,nnet);
% for i=1:nnet
%     load(['..\Data\Embedding_vector\MashUp\diff',num2str(i),',.mat'],'tA');
%     diff{i} = tA;
% end
R_sum = 0;
nnode =size(diff{i},1);
alpha = 1/(nnode);
for i=1:nnet
    QA = log(diff{i}+alpha)-log(alpha);
    R_sum = R_sum + QA*QA';
end

dim = 100;
R_sum = sparse(R_sum);
[U,S] = svds(R_sum,dim);
LA = U;
x = LA*sqrt(sqrt(S));
y = LA;

D = squareform(1-pdist(y,'cosine'));
%
% file_head = 'dream_ch2';
% embed_file = ['../Data/Embedding_vector/MashUp/',char(file_head),num2str(dim),'.x'];
% US = dlmread(embed_file);
% thres_l = [0.9,0.8,0.7];
%
% output_path = '../Data/Network/embed_network/subch2/';
%
% [nnode,ndim] = size(US);
%
% D = squareform(1-pdist(US,'cosine'));
%
% size(D)
%
% for thres = thres_l
%     D_sub = D.*(D>thres);
%     [i,j,v] = find(D_sub);
%     if ~exist(output_path, 'dir')
%         mkdir(output_path);
%     end
%     file_name = [output_path,file_head,num2str(thres)];
%     fid=fopen(file_name,'wt');
%     nedge = length(i);
%     for k=1:nedge
%         fprintf(fid,'%s\t%s\t%f\n',char(values(i2g,num2cell(i(k)))),char(values(i2g,num2cell(j(k)))),v(k));
%     end
%     fclose(fid);
%     fprintf('thres=%f,nedge=%d\n',thres,nedge);
% end