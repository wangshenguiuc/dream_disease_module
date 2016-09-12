function construct_network(US,gene_map_id,file_head,thres_l,output_path)

if ~exist('thres_l', 'var'); thres_l =  0.9:-0.1:0.1; end
if ~exist('output_path', 'var'); output_path =  '../Data/Network/embed_network/our_network/'; end
[nnode,ndim] = size(US);

D = squareform(1-pdist(US,'cosine'));

size(D)

for thres = thres_l
    D_sub = D.*(D>thres);
    [i,j,v] = find(D_sub);
    if ~exist(output_path, 'dir')
        mkdir(output_path);
    end
    file_name = [output_path,file_head,num2str(thres)];
    fid=fopen(file_name,'wt');
    nedge = length(i);
    for k=1:nedge
        fprintf(fid,'%s\t%s\t%f\n',char(values(gene_map_id,num2cell(i(k)))),char(values(gene_map_id,num2cell(j(k)))),v(k));
    end
    fclose(fid);
    fprintf('thres=%f,nedge=%d\n',thres,nedge);
end

end

