using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.ProjectOxford.Face;
using Microsoft.ProjectOxford.Face.Contract;

namespace Uploader
{
    class Program
    {
        const int PersonCount = 10000;
        const int CallLimitPerSecond = 10;
        static Queue<DateTime> _timeStampQueue = new Queue<DateTime>(CallLimitPerSecond);
        const string personGroupId = "14ac938c-bb57-40ea-9c68-1665c33da400";
        const string personGroupName = "HackathonPeeps";

        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Error: You must provide a directory path.");
                return;
            }

            string path = args[0];

            if (!Directory.Exists(path))
            {
                Console.WriteLine($"Directory {path} does not exist.");
                return;
            }


            if (!Directory.EnumerateFiles(path, "*.jpg", SearchOption.AllDirectories).Any())
            {
                Console.WriteLine($"Found no .jpg files inside of directory {path}");
                return;
            }

            try
            {
                UploadPeople(path).Wait();
            }
            catch { }

            Train().Wait();
        }

        private static FaceServiceClient CreateClient()
        {
            Console.WriteLine("Creating client");
            return new FaceServiceClient("ad4f221bdc5d4f9cbda2b41a62c66f1e", "https://westcentralus.api.cognitive.microsoft.com/face/v1.0");
        }

        private static async Task Train()
        {
            Console.WriteLine("Training...");
            var faceServiceClient = CreateClient();
            await faceServiceClient.TrainPersonGroupAsync(personGroupId);
            TrainingStatus trainingStatus = null;
            while (true)
            {
                trainingStatus = await faceServiceClient.GetPersonGroupTrainingStatusAsync(personGroupId);

                if (trainingStatus.Status != Status.Running)
                {
                    break;
                }

                await Task.Delay(1000);
            }

            Console.WriteLine("Done Training.");
        }

        static async Task UploadPeople(string root)
        {
            var faceServiceClient = CreateClient();
            _timeStampQueue.Enqueue(DateTime.UtcNow);

            Console.WriteLine("Deleting old group");
            await faceServiceClient.DeletePersonGroupAsync(personGroupId);

            Console.WriteLine("Creating Person Group");
            await faceServiceClient.CreatePersonGroupAsync(personGroupId, personGroupName);

            var dirs = Directory.GetDirectories(root);

            CreatePersonResult[] persons = new CreatePersonResult[dirs.Length];


            for(int i = 0; i < dirs.Length; i ++)
            {
                await WaitCallLimitPerSecondAsync();

                string personName = dirs[i].Split('\\').Last();

                Console.WriteLine($"Creating person {personName}");
                persons[i] = await faceServiceClient.CreatePersonAsync(personGroupId, personName);
                Console.WriteLine($"Person id for {personName} is {persons[i].PersonId}");
            }


            Console.WriteLine("Uploading images");
            for(int i = 0; i < PersonCount; i ++)
            {
                Guid personId = persons[i].PersonId;
                string personImageDir = dirs[i];

                var files = Directory.GetFiles(personImageDir, "*.jpg");
                Console.WriteLine($"Image count for {dirs[i].Split('\\').Last()}: {files.Length}");

                foreach (string imagePath in files)
                {
                    await WaitCallLimitPerSecondAsync();

                    using (Stream stream = File.OpenRead(imagePath))
                    {
                        Console.WriteLine($"    Uploading {imagePath}");
                        try
                        {
                            await faceServiceClient.AddPersonFaceAsync(personGroupId, personId, stream);
                        }
                        catch(Exception e)
                        {
                            Console.WriteLine(e);
                        }
                            await Task.Delay(TimeSpan.FromSeconds(4));
                    }
                }
            }
        }



        static async Task WaitCallLimitPerSecondAsync()
        {
            Monitor.Enter(_timeStampQueue);
            try
            {
                if (_timeStampQueue.Count >= CallLimitPerSecond)
                {
                    TimeSpan timeInterval = DateTime.UtcNow - _timeStampQueue.Peek();
                    if (timeInterval < TimeSpan.FromSeconds(1))
                    {
                        await Task.Delay(TimeSpan.FromSeconds(1) - timeInterval);
                    }
                    _timeStampQueue.Dequeue();
                }
                _timeStampQueue.Enqueue(DateTime.UtcNow);
            }
            finally
            {
                Monitor.Exit(_timeStampQueue);
            }
        }
    }
}
