using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.ProjectOxford.Face;
using Microsoft.ProjectOxford.Face.Contract;

namespace Identify
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
                Console.WriteLine("Must provide a path for the image.");
                return;
            }

            string path = args[0];
            if (!File.Exists(path))
            {
                Console.WriteLine($"File {path} does not exist!");
                return;
            }

            var task = Identify(path);
            task.Wait();
        }

        private static FaceServiceClient CreateClient()
        {
            Console.WriteLine("Creating client");
            return new FaceServiceClient("ad4f221bdc5d4f9cbda2b41a62c66f1e", "https://westcentralus.api.cognitive.microsoft.com/face/v1.0");
        }

        private static async Task Identify(string path)
        {
            FaceServiceClient faceServiceClient = CreateClient();
            string testImageFile = path;
            using (Stream s = File.OpenRead(testImageFile))
            {
                var faces = await faceServiceClient.DetectAsync(s);
                var faceIds = faces.Select(face => face.FaceId).ToArray();

                var results = await faceServiceClient.IdentifyAsync(personGroupId, faceIds);
                foreach (var identifyResult in results)
                {
                    Console.WriteLine("Result of face: {0}", identifyResult.FaceId);
                    if (identifyResult.Candidates.Length == 0)
                    {
                        Console.WriteLine("No one identified");
                    }
                    else
                    {
                        // Get top 1 among all candidates returned
                        var candidateId = identifyResult.Candidates[0].PersonId;
                        var person = await faceServiceClient.GetPersonAsync(personGroupId, candidateId);
                        Console.WriteLine($"Identified as {person.Name} with confidence of {identifyResult.Candidates[0].Confidence}");
                    }
                }
            }
        }
    }
}
