using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TESTWindowFormAPP
{
    public partial class Form1 : Form
    {
        List<String> Result;
        List<String> ContextS;
        public Form1()
        {
            InitializeComponent();
            Result = new List<String>();
            ContextS = new List<String>();
            progressBar1.Maximum = 100;
            progressBar1.Minimum = 0;
            progressBar1.Value = 0;
            progressBar1.Step = 1;
            backgroundWorker1.WorkerReportsProgress = true;
            listView1.View = View.Details;
            listView1.GridLines = true;

        }

        private void Start_Click(object sender, EventArgs e)
        {

            String SearchString = SearchStr.Text;

            if (SearchString.Length != 0) {
                Result.Clear();
                ContextS.Clear();
                listView1.Items.Clear();
                backgroundWorker1.RunWorkerAsync(SearchString);

            }
            //ShowDialog();
        }


        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            String S = (String)e.Argument;
            string currentPath = System.Environment.CurrentDirectory;
            var files = Directory.GetFiles(currentPath, "*.html");
            int all = files.Length;
            float ii = 1;

            foreach (var file in files)
            {
                try
                {   // Open the text file using a stream reader.
                    using (StreamReader sr = new StreamReader(file))
                    {
                        String line = sr.ReadToEnd();
                        int process = (int)((ii / all) * 100);
                        //System.Diagnostics.Debug.WriteLine(String.Format("{0}", process));
                        //MessageBox.Show(String.Format("{0}",process));
                        backgroundWorker1.ReportProgress(process);
                        int pos = line.IndexOf(S);
                        if (pos != -1)
                        {
                            Result.Add(file);
                            ContextS.Add(line.Substring(pos - 25 <0?0:pos - 25, 50));
                        }
                        ii += 1;
                    }
                }
                catch (Exception ep)
                {
                    Console.WriteLine("The file could not be read:");
                    Console.WriteLine(ep.Message);
                }
            }
        }

        private void backgroundWorker1_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            progressBar1.Value = e.ProgressPercentage;
        }

        private void backgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            for (int index =0;index<Result.Count;index++)
            {
                String R = Result[index];
                ListViewItem Item = new ListViewItem();
                ListViewItem.ListViewSubItem SubItem = new ListViewItem.ListViewSubItem();
                SubItem.Text = ContextS[index];
                Item.SubItems.Add(SubItem);
                listView1.Items.Add(Item);
                Item.Text = R;
            }
            listView1.EndUpdate();
        }



        private void resultListBox_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            if (listView1.SelectedItems.Count != 0)
            {
                String Value = listView1.SelectedItems[0].Text;
                //MessageBox.Show(Value);
                System.Diagnostics.Process.Start(Value);
            }

        }

        private void Form1_SizeChanged(object sender, EventArgs e)
        {

        }
    }
}
