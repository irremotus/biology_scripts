#
# This code is licensed under the MIT license.  Please see LICENSE.txt
#

import sys

if len(sys.argv) < 2:
    print("Usage: {:s} --profiles <list of profile names> --ids <list of id file names>".format(sys.argv[0]))
    exit(1)

profile_filenames = []
ids_filenames = []
profile_mode = False
ids_mode = False
for arg in sys.argv:
    if arg == "--profiles":
        profile_mode = True
        ids_mode = False
    elif arg == "--ids":
        ids_mode = True
        profile_mode = False
    elif profile_mode:
        profile_filenames.append(arg)
    elif ids_mode:
        ids_filenames.append(arg)

if len(profile_filenames) > len(ids_filenames):
    single_ids_file = True
else:
    single_ids_file = False

print("profiles:")
for p in profile_filenames:
    print("\t" + p)
print("ids:")
if single_ids_file:
    print("\t" + "Single id file: " + ids_filenames[0])
else:
    for p in ids_filenames:
        print("\t" + p)

for fileidx in range(len(profile_filenames)):
    # get filename from command line
    ifilename = profile_filenames[fileidx]
    # make output filename from input filename
    ofilename = ifilename + ".output.txt"

    if single_ids_file:
        idfilename = ids_filenames[0]
    else:
        idfilename = ids_filenames[fileidx]

    # open the files
    ifile = open(ifilename, 'r')
    ofile = open(ofilename, 'w')
    idfile = open(idfilename, 'r')

    # read the whole input file, then close it
    lines = ifile.readlines()
    ifile.close()

    idlines = idfile.readlines()
    idfile.close()

    idlist = []
    for line in idlines:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == 'R':
            parts = line.split(', ')
            for p in parts:
                if 'Gene ID' in p:
                    geneid = p.split(' ')[0]
                    idlist.append(geneid)
                else:
                    idlist.append("No Gene ID")


    # find how many of each category
    # the two categories are in line 3 == line index 2 (0 based indexing)
    cats = lines[2]
    # split the line on tabs
    data = cats.split("\t")
    # the first category starts in column index 1
    cat1 = data[1]
    # we don't know the second category yet
    cat2 = ""
    # we start with 0 of each category
    cat1c = 0
    cat2c = 0
    # go through the columns in the category line, starting with column index 1 to skip the first column (0)
    for d in data[1:]:
        # strip away whitespace on left and right
        d = d.strip()
        # if we still have data after stripping, then process it
        if len(d) > 0:
            # check if this column is category 1 -- if it is, then count it
            if d == cat1:
                cat1c += 1
            # this happens when we reach the first column of category 2
            elif cat2 == "":
                cat2 = d
                cat2c += 1
            # check if this column is category 2 -- if it is, then count it
            elif d == cat2:
                cat2c += 1

    # go through the lines of data
    dataidx = -1
    for line in lines[5:]:
        dataidx += 1
        # split the line on tabs
        data = line.split("\t")
        # if the line is empty, go to the next one
        if len(data[0].strip()) == 0:
            continue
        
        # sum the first category
        cat1sum = 0
        # calculate start and end of category 1
        start = 1
        end = start + cat1c
        # go through the columns of category 1
        for d in data[start:end]:
            # try parsing it as a number
            try:
                cat1sum += float(d.strip())
            # if it fails, ignore it (this is the "null" case)
            except ValueError:
                pass # pass does absolutely nothing -- just a placeholder

        # sum the second category
        cat2sum = 0
        # calculate start and end of category 2
        start = end
        end = start + cat2c
        # go through the columns of category 2
        for d in data[start:end]:
            # try parsing it as a number
            try:
                cat2sum += float(d.strip())
            # if it fails, ignore it (this is the "null" case)
            except ValueError:
                pass # pass does absolutely nothing -- just a placeholder

        # find averages
        cat1avg = cat1sum / cat1c
        cat2avg = cat2sum / cat2c

        # write output
        # three different cases
        if cat1avg > cat2avg:
            ofile.write("up          ")
        elif cat1avg < cat2avg:
            ofile.write("down        ")
        else:
            ofile.write("no_variation")

        curid = idlist[dataidx]
        nogenetext = "No Gene ID"
        if curid == 'No Gene ID':
            ofile.write("\t\t" + nogenetext)
        else:
            ofile.write("\t" + curid + "\t")

        gene_id = data[0].strip()

        try:
            gene_title = data[cat1c+cat2c+1].strip()
            if (len(gene_title) == 0):
                raise Exception("no gene")
        except Exception:
            gene_title = "None given"

        # write the extra data
        ofile.write("\t" + gene_id + "\t" + gene_title + "\t")
        # and the newline
        ofile.write("\n")

    # close the output file
    ofile.close()
    # print the name of the output file
    print(ofilename)
